
import flet as ft

class BatteryApp(ft.Row):
    def __init__(self): 
        
        
        self.power_state_lookup = {
            True: "On",
            False: "Off"
        }
        self.control_width = 150
        
        self.get_data = ft.ElevatedButton(
            "Get Data",
            width=self.control_width,
            height=50,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=self.get_data_click,
        )
        self.pack_pct = ft.TextField(
            label="Pack %",
            value="78",
            width=self.control_width,
        )
        self.pack_v = ft.TextField(
            label="Pack Voltage",
            value="11.94",
            width=self.control_width,
        )
        self.cell_1_v = ft.TextField(
            label="Cell 1 Voltage",
            value="4.05",
            width=self.control_width,
        )
        self.cell_2_v = ft.TextField(
            label="Cell 2 Voltage",
            value="4.05",
            width=self.control_width,
        )
        self.cell_3_v = ft.TextField(
            label="Cell 3 Voltage",
            value="4.05",
            width=self.control_width,
        )
        self.stat_1 = ft.TextField(
            label="Stat 1",
            value="??",
            width=self.control_width,
        )
        self.stat_2 = ft.TextField(
            label="Stat 2",
            value="??",
            width=self.control_width,
        )
        self.stat_3 = ft.TextField(
            label="Stat 3",
            value="??",
            width=self.control_width,
        )
        self.mode_checkbox = ft.Checkbox(
            label="Send Raw Data",
            on_change=self.mode_changed,
        )
        self.interval_checkbox = ft.Checkbox(
            label="Use send interval",
            on_change=self.interval_changed,
        )
        self.reserved_checkbox = ft.Checkbox(
            label="reserved",
            disabled=True,
            on_change=self.reserved_changed,
        )
        
        # always last
        self.controls.append(self.build())
        
    def get_data_click(self, e):
        print("Getting battery data from ESP")
        
    def mode_changed(self, e):
        print(f"Mode changed to {self.power_state_lookup[e.control.value]}")
        
    def interval_changed(self, e):
        print(f"Interval changed to  {self.power_state_lookup[e.control.value]}")
        
    def reserved_changed(self, e):
        print(f"Reserved changed to  {self.power_state_lookup[e.control.value]}")
        
        
        
        
        
    def build(self):
        return ft.Row(
            controls = [
                ft.Column(
                    controls = [
                        self.get_data,
                        self.cell_1_v,
                        self.stat_1,
                        self.reserved_checkbox,
                    ],
                ),
                ft.Column(
                    controls = [
                        self.pack_pct,
                        self.cell_2_v,
                        self.stat_2,
                        self.mode_checkbox,
                    ],
                ),
                ft.Column(
                    controls = [
                        self.pack_v,
                        self.cell_3_v,
                        self.stat_3,
                        self.interval_checkbox,
                    ],
                ),
            ],
        )
    
    




def main(page: ft.Page):
    app = BatteryApp()
    page.title = "Battery App v0.1"
    page.window.width = 500
    page.window.height = 280
    page.add(app)

# Run the Flet app
if __name__ == "__main__":
    ft.app(target=main)
