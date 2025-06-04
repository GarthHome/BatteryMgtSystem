# file:database_interface_config.py

from collections import namedtuple

#named tuples
Lut_Limits = namedtuple("Lut_Limits", ("circuit_name", "lower_limit",
                                               "upper_limit", "length"))
Config = namedtuple("Config", ("id", "owner", "app_id", "app_desc", "channel_id", "channel_description", "version_id","version_description",
                                "creation_time","mosfet","mosfet_type" ,"tempC", "r1","r2","rp","rg","LUT_CALIBRATED", "LUT") )
Short_Record = namedtuple("Short_Record",("id", "owner", "app_desc", "version_desc", "channel_id", "channel_desc"))

Columns= ["id","OWNER", "APP_ID", "APP_DESC", "CHANNEL_ID","CHANNEL_DESC","VERSION_ID","VERSION_DESC","TIMESTAMP","MOSFET_ID","MOSFET_TYPE","TEMPC","R1","R2","RP","RG","LUT_CALIBRATED","LUT"]
values=["id","owner", "app_id", "app_desc",  "channel_id", "channel_description", "version_id", "version_description", "creation_time", "mosfet_id", "mosfet_type", "tempC", "r1","r2","rp","rg", "calibrated", "LUT"]

db_path ='/Users/garth/Programming/MicroPython/usb/ryan/voltage_divider/data/rt_db'
table = 'RT_CONFIG'
#Schema: CREATE TABLE RT_CONFIG (ID INTEGER PRIMARY KEY , channel_id integer,CHANNEL_DESC VARCHAR  VERSION_ID INTEGER NOT NULL, VERSION_DESC VARCHAR,  TIMESTAMP INTEGER,  MOSFET_ID INTEGER, MOSFET_TYPE VARCHAR, TEMPC REAL, R1 REAL, R2 REAL, RP REAL, RG REAL, LUT_CALIBRATED INTEGER, LUT VARCHAR);
