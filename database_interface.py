#file: database_interface.py
''' This class will retrieve and store information for the DataController which supplies info to the GUIs.
Transactions are used when writing to the db. Each fetch method will include the tuple_factory to be
used to convert the row values to a namedtuple: one of: [_short_namedtuple_factory, _config_namedtuple_factory]'''
import sqlite3
import time
#import json
from database_interface_config import  Config, Short_Record, Columns, db_path

class DatabaseInterface:
    def __init__(self):
        self.db_path = db_path
       

#     def disconnect_from_db(self):
#         #self.cu.close()
#         self.cx.close()
    
    def _short_namedtuple_factory(self, cursor, row):
        ''' Returns row as a Short_Record:
           Short_Record = namedtuple("Short_Record",("id", "owner", "app_desc", "version_desc", "channel_id", "channel_desc"))
        '''
        return Short_Record(*row)
 
    def _config_namedtuple_factory(self, cursor, row):
        ''' Returns row as a  Config:
           Config = namedtuple("Config", ("id", "owner", "app_id", "app_desc", "channel_id", "channel_description",
                                                                "version_id","version_description", "creation_time","mosfet",
                                                                "mosfet_type" ,"tempC", "r1","r2","rp","rg","LUT_CALIBRATED", "LUT") )
       '''
        return Config(*row)
 
    def list_all_choices(self):
        '''tuple_factory is the function that specifies the namedtuple to use in creating objects from *row
          For now it is: _short_namedtuple_factory'''
        self.cx =  sqlite3.connect(self.db_path)
        self.cx.isolation_level = None
        cu = self.cx.cursor()
        self.cx.row_factory=self._short_namedtuple_factory
        select_str = 'SELECT id, owner, app_desc, channel_id, channel_desc, version_desc  FROM RT_CONFIG order by owner and channel_id;'
        records = []
        for row in cu.execute(select_str) :
            records.append(row)
        #print("records: ", records)
        return records
        
    def load_config(self, ids):
        '''tuple_factory is the function that specifies the namedtuple to use in creating objects from *row
          For this select, it is one of: [_short_namedtuple_factory, _config_namedtuple_factory]'''
        cfg=[]
        self.cx =  sqlite3.connect(self.db_path)
        self.cx.isolation_level = None
        self.cx.row_factory=self._config_namedtuple_factory
        cu = self.cx.cursor()
        select_str=f"SELECT * FROM RT_CONFIG where  id in {ids} ORDER BY CHANNEL_ID;"
        print("select_str: ", select_str)
        #Each row is a channel.
        for row in cu.execute(select_str) :
            #print("row: ", row)
            cfg.append(row)
        return cfg
    
    
    def create_next_version_records(self):
        '''Creates  new records which will store a new version of  LUT for each channel. TBD'''
        pass
    
    def save_config(self):
        pass
    
#     def store_lut(self, lut_json, channel_id, version_id, version_desc):
#         '''Stores a new record in rt_config table. values are for whole row but some are replaced with new info'''
#         #TODO: Needs testing...
#         columns= tuple(Columns)
#         values=[self.cfg]
#         values[1]=version_id
#         values[2]=version_desc
#         values[4]=channel_id
#         values[5]=int(time.time())
#         values[12]=lut_json
#         values=tuple(values)
#         print(columns, values)    
#         insert_str =f"INSERT INTO RT_CONFIG {Columns}{values}"
#         print("insert_str: ", insert_str)
#         self.cu.execute("begin")
#         self.cu.execute(insert_str)
#         self.cu.execute("commit") 
        #TODO 1: Problem: db is locked when I go to cli to check the results. # TODO 1: Fixed! use transaction . 

    def save_data(self):
        pass
    
  
