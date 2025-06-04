Instructions for sqlite3 database, db
to start on existing vb file: sqlite3 db  (lots of tables, some are not needed on the esp32)
to start a new db :  sqlite3 db_rt        (lean db with only tables needed on the esp32)
only download db_rt to the Esp32 flash.
do all sql operations to create and load tables in host. (then download db_rt to flash.)


For Lookup records:
store csv file to reflect vm-vb pairs for different situations (eg: tempc, circuit parameters, battery configuration, etc)
name the csv file to represent the circumstances. eg: lu_1_1_0_2_15.csv=> app=1,lut_id, circuit_id, mosfet_id, tempc_id.
Convert csv to a dict of vm-vb pairs.
Convert dict to json string.
paste the json string into the Lookup.lut value with keys to represent the circumstances;
Use file /data/db_create_load_tables.sql to copy paste sql statements.
Lookup schema: CREATE TABLE RT_CONFIG ... copy from above file.
Example of insert:
         INSERT into RT_CONFIG values (NULL,... copy from above file.
  
