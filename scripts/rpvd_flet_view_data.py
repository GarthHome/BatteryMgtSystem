# file: rpvd_flet_view_data.py


import flet
from flet import AppBar, ElevatedButton, Page, Text, View, Colors, DataTable
from database_interface import DatabaseInterface
from collections import namedtuple
from data_controller import DataController

# See Views (Routes) for Webserver at:

Short_Record = namedtuple(
    "Short_Record",
    ("id", "owner", "app_desc", "version_desc", "channel_id", "channel_desc"),
)
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
#Global Variables
db_path = "/Users/garth/Programming/MicroPython/usb/ryan/voltage_divider/data/rt_db"
selected_ids = set()
calibrated_rows = set()
calibrated_luts=set()
dc = DataController()


def main(page: Page):
    """Routes/Views for RPVD"""
    page.title = "Battery Management"
    page.scroll=flet.ScrollMode.ALWAYS
    page.window.width=800
    dc.cfg=dc.list_all_choices()
    print("Initial route:", page.route)

    def random_row( vin, vm0):
        '''Returns a mock 7-tuple, "randomized row",  given the input voltage.
        In mock, the calibrated value is always zero. This function will be replaced
        In the real world  where 4 of the 7-tuple come from
        DataController.calibrate(vin) function and where calibrate can be one of [0,1]   '''
        global row_id,dc
        row_id += 1
        vm= vm0 + random.randint(-5,5)/10 *122e-6
        sd= random.randint(-5,5)*122e-6
        vb= vin/vm0 * vm
        err= vb-vin
        if abs(err) < dc.limit :
            calibrated = True
        else:
            calibrated = False
        row_tuple = (row_id, vin, vm, sd, vb, err, calibrated)
        #print("row_tuple: ", row_tuple)
        return row_tuple
    
    def save_id(e):
        """A checkbox was set to true. Set the row number as one of a three-tuple"""
        #print("selected :", e.control.data)
        selected_ids.add(e.control.data)

    def mark_as_calibrated(e):
        '''Adds or removes row numbers from calibrated_rows global variable
         checkbox {'label': '1 calibrated', 'value': 'true'} '''
        global calibrated_rows
        row=int(e.control.label[0:2])
        val= e.control.value
        print(f" {e.control} ")
        if val:
            calibrated_rows.add(row)
        else:
             calibrated_rows.remove(row)
        print("calibrated rows: ", calibrated_rows)

    def get_configuration(e):
        global  dc, selected_ids
        ids= tuple(sorted(selected_ids))
        print(f"Requested fetch of configuration records: {e.control}")
        print("get_configuration.selected_ids: ", ids)
        dc.load_config(ids)
        #print("dc.cfg: ", dc.cfg)

    # TODO 11:  implement the lut downloads...
    def download_lut_0(e):
        pass

    def download_lut_1(e):
        pass

    def download_lut_2(e):
        pass
    # Short_Record fields:  id, owner, app_desc, version_desc", channel_id, channel_desc,
    def build_columns():
        columns = [
            flet.DataColumn(flet.Text("id")),
            flet.DataColumn(flet.Text("owner")),
            flet.DataColumn(flet.Text("app_desc")),
            flet.DataColumn(flet.Text("version_desc")),
            flet.DataColumn(flet.Text("channel_id")),
            flet.DataColumn(flet.Text("channel_desc")),
        ]
        return columns

    def build_rows():
        global dc
        """Returns a list of flet.DataRow. A DataRow is a list of flet.DataCell. A DataCell holds a flet.Control with data value"""
        rows = []
        all_records=dc.cfg
        #print("dc.cfg : ", dc.cfg)
        #print("all records : ", all_records)
        # print("First record: ", all_records[0])
        for r in all_records:
            cells = []
            rid=r[0]
            rowner=r[1]
            rapp_desc=r[2]
            rchanid=r[3]
            rchandesc=r[4]
            rversdesc=r[5]
            # First r serves as header record, hence checkbox does not return row id
            cells.append(
                flet.DataCell(flet.Checkbox(f"{rid}", data=rid, on_change=save_id))
            ),
            cells.append(flet.DataCell(Text(rowner))),
            cells.append(flet.DataCell(Text(rapp_desc))),
            cells.append(flet.DataCell(Text(rchanid))),
            cells.append(flet.DataCell(Text(rchandesc))),
            cells.append(flet.DataCell(Text(rversdesc))),
            rows.append(flet.DataRow(cells))
        #print("Returning rows: ", rows)
        return rows

    # ("id", "owner", "app_id", "app_desc", "channel_id", "channel_description", "version_id","version_description",
    #  "creation_time","mosfet","mosfet_type" ,"tempC", "r1","r2","rp","rg","LUT_CALIBRATED", "LUT") )

    def build_config_columns():
        columns = [
            flet.DataColumn(flet.Text("id")),
            flet.DataColumn(flet.Text("owner")),
            flet.DataColumn(flet.Text("app_id")),
            flet.DataColumn(flet.Text("app_desc")),
            flet.DataColumn(flet.Text("channel_id")),
            flet.DataColumn(flet.Text("channel_desc")),
            flet.DataColumn(flet.Text("version_id")),
            flet.DataColumn(flet.Text("version_desc")),
            flet.DataColumn(flet.Text("creation_time")),
            flet.DataColumn(flet.Text("mosfet_id")),
            flet.DataColumn(flet.Text("mosfet_type")),
            flet.DataColumn(flet.Text("tempC")),
            flet.DataColumn(flet.Text("r1")),
            flet.DataColumn(flet.Text("r2")),
            flet.DataColumn(flet.Text("rp")),
            flet.DataColumn(flet.Text("rg")),
            flet.DataColumn(flet.Text("lut_calibrated")),
            flet.DataColumn(flet.Text("lookup_table")),
        ]
        return columns

    def build_config_rows():
        rows = []
        print(
            "matching records : ",
        )
        #    "id", "owner", "app_id", "app_desc","channel_id", "channel_desc","version_id", "version_desc",
        #    "creation_time","mosfet", "mosfet_type", "tempC","r1","r2", "rp","rg", "LUT_CALIBRATED", "LUT",
        for r in config_records:
            cells = []
            cells.append(flet.DataCell(Text(r.id))),
            cells.append(flet.DataCell(Text(r.owner))),
            cells.append(flet.DataCell(Text(r.app_id))),
            cells.append(flet.DataCell(Text(r.app_desc))),
            cells.append(flet.DataCell(Text(r.channel_id))),
            cells.append(flet.DataCell(Text(r.channel_desc))),
            cells.append(flet.DataCell(Text(r.version_id))),
            cells.append(flet.DataCell(Text(r.version_desc))),
            cells.append(flet.DataCell(Text(r.creation_time))),
            cells.append(flet.DataCell(Text(r.mosfet_id))),
            cells.append(flet.DataCell(Text(r.mosfet_type))),
            cells.append(flet.DataCell(Text(r.tempC))),
            cells.append(flet.DataCell(Text(r.r1))),
            cells.append(flet.DataCell(Text(r.r2))),
            cells.append(flet.DataCell(Text(r.rp))),
            cells.append(flet.DataCell(Text(r.rg))),
            cells.append(
                flet.DataCell(
                    flet.Checkbox(f"{r.calibrated}", data=i, on_change = mark_as_calibrated, value=r.calibrated)
                )
            ),
            rows.append(flet.DataRow(cells))
        #print("Returning rows: ", rows)
        return rows

    def build_lut_calibrate_datatable(channel):
        global dc
        dc.row_id=0
        lut= dc.luts[channel]
        vins = dc.luts[channel].values()
        #print("dc.luts[channel]: ", dc.luts[channel])
        #print("vins: ", vins)
        calib_columns = [
            flet.DataColumn(flet.Text("id")),
            flet.DataColumn(flet.Text("vin")),
            flet.DataColumn(flet.Text("vm")),
            flet.DataColumn(flet.Text("sd")),
            flet.DataColumn(flet.Text("vb")),
            flet.DataColumn(flet.Text("err")),
            flet.DataColumn(flet.Text("calibrated")),
        ]
        # calibrate(self, vin, channel, reps, tolerance):
        calib_rows = []
        row_id = 1
        for v in vins:
            #row_id, vin, vm, sd, vb, err, calibrated. Following creates a record statistically for now.
            ( id, vin, vm, sd, vb, err, calibrated) = dc.calibrate(v, channel, 64, 3)
            #print("from dc.calibrate ",id,vin,vm,sd,vb,err,calibrated)
            if calibrated:
                calibrated_rows.add(id)
            cells = []
            cells.append(flet.DataCell(Text(f"{id}"))),
            cells.append(flet.DataCell(Text(v))),  # vin
            cells.append(flet.DataCell(Text(vm))),  # vm
            cells.append(flet.DataCell(Text(sd))),  # sd
            cells.append(flet.DataCell(Text(vb))),  # vb
            cells.append(flet.DataCell(Text(err))),  # err
            cells.append(flet.DataCell(flet.Checkbox(f"{id} " , value=calibrated, data= calibrated, on_change=mark_as_calibrated))),
            calib_rows.append(flet.DataRow(cells))
            row_id += 1
        if len(calibrated_rows) == len(vins):
            calibrated_luts.add(channel)
        return(flet.DataTable(calib_columns, calib_rows))
           
    def route_change(e):
        global  dc
        print("Route change:", e.route)
        #print("route_changed, cfg: ", dc.cfg[0][1]) 
        page.views.clear()
        #page.views.scroll=flet.ScrollMode.ALWAYS
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Battery Management")),
                    #Text("App_Owner"),
                    #Text(dc.cfg[0][1]),
                    Text(f"Calibrated Lookup Tables:  {calibrated_luts}" ),
                    ElevatedButton("Select Configuration", on_click=open_config),
                ],
            )
        )
        if (
            page.route == "/config"
            or page.route == "/config/0"
            or page.route == "/config/1"
            or page.route == "/config/2"
        ):
            page.views.append(
                View(
                    "/config",
                    [
                        AppBar(title=Text("Configuration"), bgcolor=Colors.BLACK),
                        #Text("App_Owner"),
                        #Text(dc.cfg[0][1]),
                        Text("Config!", style="bodyMedium"),
                        Text("Choose ids for configuration using checkboxes", visible=True, disabled=False),
                        flet.DataTable(
                            width=700, columns=build_columns(), rows=build_rows()
                        ),
                        flet.Row(
                            controls=[
                                ElevatedButton(
                                    "Get Config_records", disabled=False, visible=True, on_click=get_configuration
                                ),
                                ElevatedButton(
                                    "Go to 4.2 V config", on_click=open_channel_0
                                ),
                                ElevatedButton(
                                    "Go to 8.4 V config", on_click=open_channel_1
                                ),
                                ElevatedButton(
                                    "Go to 12.6 V config", on_click=open_channel_2
                                ),
                            ]
                        ),
                    ],
                )
            )
        if page.route == "/config/0" or page.route == "config/":
            page.views.append(
                View(
                    "/config/0",
                    [
                        AppBar(title=Text("4.2 V channel 0"), bgcolor=Colors.BLACK),
                        flet.Row(controls=[Text('Owner:'), Text(dc.cfg[0][1])]),
                        ElevatedButton(
                            "Calibrate 4.2 V Lookup Table",
                            on_click=open_channel_0_lut_calibrate,
                        ),
                        ElevatedButton(
                            "Measure using 4.2 V Lookup Table",
                            on_click=open_channel_0_lut_measure,
                        ),
                             ElevatedButton(
                            "Download 4.2 V Lookup Table",
                            on_click=open_channel_0_lut_download,
                            ),
                    ],
                )
            )
        if page.route == "/config/0/lut_calibrate" or page.route == "config/0":
            page.views.append(
                View(
                    "/config/0/lut_calibrate",
                    [
                        AppBar(title=Text("4.2 V Lookup Table Calibrate"), bgcolor=Colors.BLACK,),
                        flet.Row(controls=[Text('Owner:'), Text(dc.cfg[0][1]),
                        Text("Calibrated_Lookup Tables:"),  Text(calibrated_luts),]),
                        
                        Text(dc.luts[0]),
                        build_lut_calibrate_datatable(0),
                    ],
                )
            )
        if page.route == "/config/0/lut_measure" or page.route == "config/0":
            # TODO 6: build measure view for LUT[0]
            page.views.append(
                View(
                    "/config/0/lut_measure",
                    [
                        AppBar( title=Text("4.2 V Lookup Table Measurement"), bgcolor=Colors.BLACK,  ),
                        flet.Row(controls=[Text('Owner:'), Text(dc.cfg[0][1])]),
                        flet.Row(controls=[Text("Calibrated_Lookup Tables:"),  Text(calibrated_luts),]),
                        Text(dc.luts[0]),
                    ],
                )
            )
        if page.route=="/config/0/lut_download":
                page.views.append(
                View(
                    "/config/0/lut_download",
                    [
                        AppBar( title=Text("4.2 V Lookup Table Download"),  bgcolor=Colors.BLACK,),
                        flet.Row(controls=[Text('Owner:'), Text(dc.cfg[0][1]) ]),
                        flet.Row(controls=[Text("Calibrated_Lookup Tables:"),  Text(calibrated_luts),]),
                        ElevatedButton( "Download ",  on_click=download_lut_0,
                        ),
                        
                        Text(dc.luts[0]),
                    ],
                )
            )
                
        if page.route == "/config/1":
            page.views.append(
                View(
                    "/config/1",
                    [
                        AppBar(title=Text("8.4 V channel 1"), bgcolor=Colors.BLACK),
                        flet.Row(controls=[Text('Owner:'), Text(dc.cfg[0][1])]),
                        flet.Row(controls=[Text("Calibrated_Lookup Tables:"),  Text(calibrated_luts),]),
                       ElevatedButton(
                            "Calibrate 8.4 V Lookup Table",
                            on_click=open_channel_1_lut_calibrate,
                        ),
                        ElevatedButton(
                            "Measure using 8.4 V Lookup Table",
                            on_click=open_channel_1_lut_measure,
                        ),
                        ElevatedButton(
                            "Download 8.4 V Lookup Table",
                            on_click=open_channel_1_lut_download,
                            ),
                    ],
                )
            )
        if page.route == "/config/1/lut_calibrate" or page.route == "config/1":
            page.views.append(
                View(
                    "/config/1/lut_calibrate",
                    [
                        AppBar(
                            title=Text("8.4 V Lookup Table Calibrate"),
                            bgcolor=Colors.BLACK,
                        ),
                        flet.Row(controls=[Text('Owner:'), Text(dc.cfg[0][1])]),
                        flet.Row(controls=[Text("Calibrated_Lookup Tables:"),  Text(calibrated_luts),]),
                        Text(dc.luts[1]),
                        build_lut_calibrate_datatable(1),
                    ],
                )
            )
        if page.route == "/config/1/lut_measure" or page.route == "config/1":
            page.views.append(
                View(
                    "/config/1/lut_measure",
                    # TODO 9: build measure view for LUT[1]

                    [
                        AppBar( title=Text("8.4  V Lookup Table Measurement"), bgcolor=Colors.BLACK, ),
                        flet.Row(controls=[Text('Owner:'), Text(dc.cfg[0][1])]),
                        flet.Row(controls=[Text("Calibrated_Lookup Tables:"),  Text(calibrated_luts),]),
                    ],
                )
            )
        if page.route == "/config/1/lut_download" or page.route == "config/1":
            page.views.append(
                View(
                    "/config/1/lut_download",
                    [
                        AppBar( title=Text("8.4  V Lookup Table Download"), bgcolor=Colors.BLACK, ),
                        flet.Row(controls=[Text('Owner:'), Text(dc.cfg[0][1])]),
                        flet.Row(controls=[Text("Calibrated_Lookup Tables:"),  Text(calibrated_luts),]),
                        ElevatedButton("Download", on_click=download_lut_1,),
                        Text(dc.luts[1])
                    ],
                   
                )
            )
        if page.route == "/config/2" or page.route == "config/":
            page.views.append(
                View(
                    "/config/2",
                    [
                        AppBar(
                            title=Text("12.6 V Lookup Table Calibrate"),
                            bgcolor=Colors.BLACK,
                        ),
                        flet.Row(controls=[Text('Owner:'), Text(dc.cfg[0][1])]),
                        flet.Row(controls=[Text("Calibrated_Lookup Tables:"),  Text(calibrated_luts),]),
                      
                        ElevatedButton(
                            "Calibrate 12.6 V Lookup Table",
                            on_click=open_channel_2_lut_calibrate,
                        ),
                        ElevatedButton(
                            "Measure using 12.6 V Lookup Table",
                            on_click=open_channel_2_lut_measure,
                        ),
                        ElevatedButton(
                            "Download 12.6 V Lookup Table",
                            on_click=open_channel_2_lut_download,
                            ),
                        Text(dc.luts[2]),
                        build_lut_calibrate_datatable(2),
                    ],
                )
            )
        if page.route == "/config/2/lut_calibrate" or page.route == "config/2":
            page.views.append(
                View(
                    "/config/2/lut_calibrate",
                    [
                        AppBar(
                            title=Text("12.6 V Lookup Table Calibrate"),
                            bgcolor=Colors.BLACK,
                        ),
                        flet.Row(controls=[Text('Owner:'), Text(dc.cfg[0][1])]),
                        flet.Row(controls=[Text("Calibrated_Lookup Tables:"),  Text(calibrated_luts),]),
                        Text(dc.luts[2]),
                        build_lut_calibrate_datatable(2),
                    ],
                )
            )
        if page.route == "/config/2/lut_measure" or page.route == "config/2":
            page.views.append(
                View(
                    "/config/2/lut_measure",
                    [
                        AppBar(
                            title=Text("12.6 V Lookup Table Measurement"),
                            bgcolor=Colors.BLACK,
                        ),
                        flet.Row(controls=[Text('Owner:'), Text(dc.cfg[0][1])]),
                        flet.Row(controls=[Text("Calibrated_Lookup Tables:"),  Text(calibrated_luts),]),
                        # TODO 10: build measure view for LUT[2]
                        Text(dc.cfg[2]),
                    ],
                )
            )
        if page.route == "/config/2/lut_download":
            page.views.append(
                View(
                    "/config/2/lut_download",
                    [
                        AppBar(title=Text("12.6 V channel 2 Download"), bgcolor=Colors.BLACK),
                        flet.Row(controls=[Text('Owner:'), Text(dc.cfg[0][1])]),
                        flet.Row(controls=[Text("Calibrated_Lookup Tables:"),  Text(calibrated_luts),]),
                        ElevatedButton("Download",  on_click=download_lut_2, ),
                        Text(dc.luts[2])
                   ],
                )
            )

        page.update()

    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    def open_channel_0_lut_calibrate(e):
        page.go("/config/0/lut_calibrate")

    def open_channel_0_lut_measure(e):
        page.go("/config/0/lut_measure")
                
    def open_channel_0_lut_download(e):
        page.go("/config/0/lut_download")

    def open_channel_1_lut_calibrate(e):
        page.go("/config/1/lut_calibrate")

    def open_channel_1_lut_measure(e):
        page.go("/config/1/lut_measure")
        
    def open_channel_1_lut_download(e):
        page.go("/config/1/lut_download")

    def open_channel_2_lut_calibrate(e):
        page.go("/config/2/lut_calibrate")

    def open_channel_2_lut_measure(e):
        page.go("/config/2/lut_measure")

    def open_channel_2_lut_download(e):
        page.go("/config/2/lut_download")
        
    def open_channel_0(e):
        page.go("/config/0")

    def open_channel_1(e):
        page.go("/config/1")

    def open_channel_2(e):
        page.go("/config/2")

    def open_config(e):
        page.go("/config")

    page.go(page.route)


flet.app(target=main, view=flet.AppView.WEB_BROWSER)
