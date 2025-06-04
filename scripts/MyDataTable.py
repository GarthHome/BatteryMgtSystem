# file: MyDataTable2.py

# file: MyDataTable.py   a class to construct a flet.DataTable and return it.

import flet as ft
from flet import Page, Text, View, Colors, DataTable
import random
from collections import namedtuple

# TODO 2: Figure out how to use this inside of rpvd_flet_view_data.py ...
# TODO 3: Get the scrolling to work so lut1 (8,4V) and lut2 (12.6 V) can be calibrated.
limit = 190e-6  # when abs(err) is less than this limit, the row is calibrated. when all rows are calibrated, the LUT is calibrated.
row_id = 0
mdt=0
lut1 = {2.02278: 6.0, 2.058313: 6.1, 2.093844: 6.2, 2.129375: 6.3, 2.164906: 6.4,
            2.197645: 6.5, 2.23: 6.6, 2.230969: 6.7, 2.26361: 6.8, 2.298156: 6.9, 2.364712: 7,
            2.402375: 7.1, 2.435156: 7.2, 2.4688: 7.3, 2.466984: 7.4, 2.503416: 7.5,
            2.538055: 7.6, 2.60425: 7.8, 2.606547: 7.7, 2.673762: 7.9, 2.706445: 8,
            2.708914: 8.1, 2.739847: 8.2, 2.773871: 8.3, 2.831112: 8.4, 2.866643: 8.5,
            2.902174: 8.6, 2.93770: 8.7, 2.973236: 8.8, 3.008767: 8.9, 3.044298: 9.0}
headers = ["row_id","Vin","edit_vm","sd","vb","err", "calibrated"]
rows=[]
columns=[]

def build_columns(headers):
        '''Returns a list of flet.DataColumn, A DataColumn holds a Text of h in headers. Arg: headers is list of strings'''
        columns=[]
        for h in headers:
            if h=="edit_vm":
                columns.append(ft.DataColumn(ft.Text(value=h, width=150)))
            else:
                columns.append(ft.DataColumn(ft.Text(h)))
        #print("columns: ", columns)
        return columns
            
def build_rows(lut, start_row_id):
    global row_id
    '''Returns list < ft.DataRow> .  A DataRow is a list < ft.DataCell>.
          A DataCell holds a ft.Control type with one of 7 values from random_row.
           ...
           c = ft.Row(
        [lvc, sw],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )'''
    #print("row_id: ", row_id)
    rows=[]
    for k, v in lut.items():
        cells =[]
        (row_id, vin, vm, sd, vb, err, calibrated) = random_row(v, k)
        cells.append(ft.DataCell(ft.Text(row_id), data=row_id,  on_double_tap=show_after))
        cells.append(ft.DataCell(ft.Text(vin)))
        cells.append(ft.DataCell(ft.TextField(value=vm, data=(vin, vm, vb), max_length= 10, width=500 ) ))
        cells.append(ft.DataCell(ft.Text(sd)))
        cells.append(ft.DataCell(ft.Text(vb)))
        cells.append(ft.DataCell(ft.Text(f"{err}", color=Colors.BLACK, bgcolor=bg_color(err, limit))))
        cells.append(ft.DataCell(ft.Checkbox( label="calibrated",   data = row_id, on_change = mark_as_calibrated, value=calibrated)))
#         print(" build_rows, start_row_id: ", start_row_id, " row_id: ", row_id)
#         if row_id < start_row_id:
#             pass
#         else:
#             rows.append(ft.DataRow(cells))
        rows.append(ft.DataRow(cells))
    #print("rows: ", rows)
    return rows
    
def build_table(columns, rows, width=150):
        '''Returns a DataTable. Can only be called when columns and rows are populated.'''
        if len(columns) != len(rows[0].cells) :
            #print("length of columns: ", len(columns), "length of rows: ", len(rows[0].cells))
            print("Each row must have the same number of cells as you have columns")
 #       return  ft.DataTable(columns, rows, width, show_bottom_border=True, scroll=ft.ScrollMode.AUTO)
        return  ft.DataTable(columns, rows, width, show_bottom_border=True)

# TODO 1: Figure out how to minimize err by adjusting vm TextField value.  

def show_after(e):
    global columns, mdt
    '''Handler called when User double_taps a row_id DataCell. The rows will update starting with the tapped row_id'''
    row_id = int(f"{e.control.data}")
    print(f"show_after row: {row_id}")
    row_id=0       #restart row_id counter
    
#     rows = build_rows(lut1, row_id)
#     mdt = build_table(rows, columns, width=150)

def random_row( vin, vm0):
        '''Returns a mock 7-tuple, "randomized row",  given the input voltage.
        In mock, the calibrated value is always zero. This function will be replaced
        In the real world  where 4 of the 7-tuple come from
        DataController.calibrate(vin) function and where calibrate can be one of [0,1]   '''
        global row_id,limit
        row_id += 1
        vm= vm0 + random.randint(-5,5)/10 *122e-6
        sd= random.randint(-5,5)*122e-6
        vb= vin/vm0 * vm
        err= vb-vin
        if abs(err) < limit :   #see line 12
            calibrated = True
        else:
            calibrated = False
        row_tuple = (row_id, vin, vm, sd, vb, err, calibrated)
        #print("row_tuple: ", row_tuple)
        return row_tuple
    
def mark_as_calibrated(e):
    print(f"Row: {e.control.data} is  {calibrated} ")
    
def bg_color(val, limit):
    if abs(val) < limit:
        bgc=Colors.GREEN_ACCENT_100
    else:
        bgc=Colors.RED_100
    return bgc

def main(page : Page):
    global rows, mdt
#     lv = ft.ListView(spacing=10, padding=20, width=150, auto_scroll=False)
#     lvc = ft.Container(
#         content=lv,
#         bgcolor=ft.Colors.GREY_500,)
    columns=build_columns(headers)
    rows = build_rows(lut1, 1)
    width = 150
    mdt = build_table(columns, rows,width)
    page.scroll=ft.ScrollMode.ALWAYS
    page.add(mdt)
    page.window.width=800
    page.update()
    
    
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
