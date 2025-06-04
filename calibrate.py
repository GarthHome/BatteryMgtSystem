# file: calibrate.py path: /Users/garth/Programming/MicroPython/scripts/ryan/ryan_voltage_divider/scripts/calibrate.py

# Close but formatting may be the problem

import flet as ft
import json
from data_controller import DataController
from database_interface import DatabaseInterface
from collections import namedtuple

dbpath = "/Users/garth/Programming/MicroPython/usb/ryan/voltage_divider/data/rt_db"
Config = namedtuple(
    "Config",
    (
        "id",
        "owner",
        "app_id",
        "app_desc",
        "channel_id",
        "channel_desc",
        "version_id",
        "version_desc",
        "creation_time",
        "mosfet",
        "mosfet_type",
        "tempC",
        "r1",
        "r2",
        "rp",
        "rg",
        "LUT_CALIBRATED",
        "LUT",
    ),
)


class CalibrateApp(ft.Row):
    """View to allow User to save vm/vb pairs to later use as a lookup/interpolator"""

    def __init__(self):
        super().__init__()

        self.ids3 = (1, 2, 3)  # kludge for now, just GM records...
        self.dc = DataController()
        self.dc.load_config(self.ids3)
        print("init self.dc.cfg: ", self.dc.cfg)
        print("init dc.luts: ", self.dc.luts)
        self.circuit_num = 0
        self.control_width = 125

        # This will be loaded with dicts from the DataController, but for now...
        self.lut = []

        # dropdowns -----=======================
        self.ddm = ft.Dropdown(
            editable=True,
            label="Mode",
            options=[
                ft.DropdownOption("Measure"),
                ft.DropdownOption("Calibrate"),
            ],
            on_change=self.ddm_changed,
        )

        self.ddc = ft.Dropdown(
            editable=True,
            label="Circuit",
            options=[
                ft.dropdown.Option("C42"),
                ft.dropdown.Option("C84"),
                ft.dropdown.Option("C126"),
            ],
            on_change=self.ddc_changed,
        )

        # push buttons=====================
        self.get_data = ft.ElevatedButton(
            "Get Data",
            width=self.control_width,
            height=25,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=self.get_data_click,
        )

        self.load_file_pb = ft.ElevatedButton(
            "Load Lut",
            width=self.control_width,
            height=25,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=self.show_lut,
        )
        self.save_file_pb = ft.ElevatedButton(
            "Save Lut",
            width=self.control_width,
            height=25,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=self.save_lut,
        )

        self.next_pb = ft.ElevatedButton(
            "Next row",
            on_click=self.get_next,
            disabled=False,
            width=self.control_width,
            height=25,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle( shape=ft.RoundedRectangleBorder(radius=10), )
        )

        self.row_id = ft.TextField(
            label="#",
            value=0,
            width=self.control_width,
            read_only="true",
        )

        self.tempc = ft.TextField(label="TempC", width=self.control_width, value=25.6)
        self.sample_size = ft.TextField(
            label="sample size ", width=self.control_width, value=32
        )

        self.tol = ft.TextField(
            label="Tolerance (σ) ", width=self.control_width, value=1.5
        )

        self.truth = ft.TextField(
            label="Battery Truth",
            # value=self.lut[self.lower_limit],
            width=self.control_width,
            read_only="true",
        )
        self.measured_v = ft.TextField(
            label="Measured Voltage",
            # value=self.lower_limit,
            width=self.control_width,
        )
        self.est_batt_v = ft.TextField(
            label="Est Batt Voltage",
            value="9.5978",
            width=self.control_width,
            read_only="true",
        )
        self.error = ft.TextField(
            label="Error",
            value="0.0078",
            width=self.control_width,
            on_change=self.change_background,
        )

        self.sd = ft.TextField(
            label="SD", value="1.23e-4", width=self.control_width, read_only="true"
        )

        self.spacer = ft.TextField(value="", width=self.control_width, read_only="true")

        # always last
        self.controls.append(self.build())

#     def limit_luts(self, lut, circuit):
#         for n in self.lut:
#             ord_keys = sorted(lut.keys())
#             lower_limit = ord_keys[0]
#             upper_limit = ord_keys[-1]
#             print("Lower Limit: ", lower_limit)
#             print("Upper Limit: ", upper_limit)
#             length = len(self.lut) - 1  # stopping value for row_id, prevents
#             self.volt_limits[circuit] = (lower_limit, upper_limit, length)
# 
    # Handlers /////////////////////////////////////
    def ddm_changed(self, e):
        """mode dropdown handler function"""
        # e.control.bgcolor=ft.Colors.LIGHT_GREEN
        print("mode selected: ", e.control.value)
        self.mode_val = e.control.value
        if e.control.value == "Calibrate":
            self.sample_size.value = 512
        else:
            self.sample_size.value = 64
        self.page.update()

    def ddc_changed(self, e):
        """The circuit dropdown value is a string eg: 'C42' . self.circuit_num is a number, one of: [0,1,2]"""
        print("circuit selected: ", e.control.value)
        circuits = ["C42", "C84", "C126"]
        self.circuit_num = circuits.index(e.control.value)
        lut = self.dc.luts[self.circuit_num]
        lut_limit = self.dc.lut_limits[self.circuit_num]
        ord_keys = sorted(lut.keys())
        self.row_id.value=0
        self.populate_fields(lut, ord_keys, 0)
        self.next_pb.disabled=False
        self.page.update()

    def get_data_click(self, e):
        circuit = self.circuit_num
        mode = self.mode_val
        sample_size = self.sample_size.value
        tol = self.tol.value
        batt_volts = self.truth.value

        print(
            f"DataController will request {mode} for battery voltage: {batt_volts} in circuit: {circuit} sample_size:  {sample_size} tolerance: {tol} \nand will return values for Vm, SD"
        )

    def change_background(self, e):
        v = float(e.control.value)
        e.control.bgcolor = ft.Colors.LIGHT_GREEN if v < 0.0004 else ft.Colors.PINK

    def get_next(self, e):
        #print(f"Getting next voltage record {e.control}")
        lut = self.dc.luts[self.circuit_num]
        #print("lut :", lut)
        #print("lut_limits: ", self.dc.show_lut_limits(self.circuit_num))
        ord_keys = sorted(lut.keys())
        rowid = int(self.row_id.value) + 1
        if rowid > len(lut) -1 :
                   print(" No more lookup values for this circuit. Done... If all calibrated, Save Lut to db.")
                   self.next_pb.disabled=True
                   self.page.update()
                   #print("Button: next_pd.disabled: ", self.next_pb.disabled)  #once page.update() is called, it is disabled.
        else:
             print("rowid", rowid)
             self.row_id.value = rowid
             self.populate_fields( lut, ord_keys, rowid)

    def populate_fields(self, lut, ord_keys, rowid):
        vm = ord_keys[rowid]
        vb = lut[vm]
        #print("next values: ", rowid, ",", vm, ", ", vb)
        # update gui page
        self.measured_v.value = vm
        self.truth.value = vb
        self.est_batt_v.value = vb + 0.0045
        self.error.value = 0.0045
        self.page.update()

    def show_lut(self, e):
        """Modified on 5/29/2025 to load config from rt_db. Already loaded, just point to correct lut"""
        print("cicuit_num: ", self.circuit_num)
        self.dc.dbi.load_config(self.ids3)
        print("self.dc.cfg: ", self.dc.cfg)
        self.lut = self.dc.luts[self.circuit_num]
        print("lut: ", self.lut)

    def save_lut(self, e):
        print("Saving LUT to file ")

    def build(self):
        return ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        self.ddm,
                        self.row_id,
                        self.get_data,
                    ],
                ),
                ft.Column(
                    controls=[
                        self.ddc,
                        self.truth,
                        self.load_file_pb,
                    ],
                ),
                ft.Column(
                    controls=[
                        self.tempc,
                        self.measured_v,
                        self.save_file_pb,
                    ]
                ),
                ft.Column(
                    controls=[
                        self.sample_size,
                        self.sd,
                        self.next_pb,
                    ],
                ),
                ft.Column(
                    controls=[
                        self.tol,
                        self.est_batt_v,
                        self.error,
                    ],
                ),
            ],
        )


def main(page: ft.Page):
    app = CalibrateApp()
    page.title = "Calibrate App v0.1"
    page.window.width = 850
    page.window.height = 280
    page.add(app)


# Run the Flet app
if __name__ == "__main__":
    ft.app(target=main)
