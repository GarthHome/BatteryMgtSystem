drop table TempC;
drop table LUTS;
drop table Application;
drop table mosfet;
drop table circuit;
drop table owner;
drop table config;

CREATE TABLE TempC (id integer primary key, tempc_id integer, tempc real);

CREATE TABLE Lookup (id integer primary key, lut_id integer, lut_desc varchar, app_id integer, circuit_id integer, mosfet_id integer, tempc_id integer, lut varchar);

CREATE TABLE Application (id integer primary key, app_id integer, desc varchar, owner_id integer );

CREATE TABLE mosfet (id integer primary key, mosfet_id integer, type varchar, rise_time real, fall_time real, overshoot_rise  real, overshoot_fall);

CREATE TABLE circuit( id integer primary key, circ_id integer, desc varchar, app_id integer, version integer, desc varchar, mosfet_id INTEGER,
R1 REAL, R2 REAL, RP real, RG real,  B_CELL_1 INTEGER, B_CELL_2 INTEGER, B_CELL_3 INTEGER);

CREATE TABLE owner( id integer primary key, owner_id integer, name varchar);

CREATE TABLE Config( id integer primary key, config_id integer, version integer, version_reason varchar, timestamp integer, owner_id integer, app_id integer, circ_id integer, mosfet_id integer, tempc_id integer)

CREATE TABLE datasheets( id integer primary key, device_id,desc varchar,  url varchar );

CREATE TABLE RT_CONFIG (ID INTEGER PRIMARY KEY , channel_id integer,CHANNEL_DESC VARCHAR  VERSION_ID INTEGER NOT NULL, VERSION_DESC VARCHAR,  TIMESTAMP INTEGER,  MOSFET_ID INTEGER, MOSFET_TYPE VARCHAR, TEMPC REAL, R1 REAL, R2 REAL, RP REAL, RG REAL, LUT VARCHAR);

insertions:
TempC:
       copy and paste results below into sqlite3 db1 shell.
       python:
          j=1;
          for i in range(-40, 125, 5):
              print(f" insert into TempC values(NULL, {j}, {i});")

       j+=1

owner:
       insert into owner values(NULL, 1, 'GM');
       insert into owner values(NULL, 2, 'RP');

 mosfet:

       insert into mosfet values(1,1,'P-channel', 700, 900, 25, 50);
circuit:
       insert into circuit values (NULL, 0, 1, 1, '4.2 Volt Circuit', 1, 328.5, 997.9, 9998.5,220.3,1,2,3)
       insert into circuit values (NULL, 1, 1, 1, '8.4 Volt Circuit', 2, 1000.5, 509.6,  10007.0, 470.0, 1, 2, 3)
       insert into circuit values (NULL, 2, 1, 1, '12.6 Volt Circuit',3, 1001.5, 329.6,  10000.0, 680.0, 1, 2, 3)

Lookup:

       insert into Lookup values (NULL, 0,'Lookup for 4.2V circuit', 1, 0, 1,15, '{"2.342736":3.2,"2.415946":3.3,"2.489157":3.4,"2.562367":3.5,"2.635578":3.6,"2.708788":3.7,"2.781999":3.8,"2.855209":3.9,"2.92842":4.0,"3.00163":4.1}');
       insert into Lookup values (NULL, 1,'Lookup for 8.4V circuit',1, 1, 1,15, '{"2.129375":6.3,"2.164906":6.4,"2.197645":6.5,"2.23":6.6,"2.230969":6.7,"2.26361":6.8,"2.298156":6.9,"2.364712":7,"2.402375":7.1,"2.435156":7.2,"2.4688":7.3,"2.466984":7.4,"2.503416":7.5,"2.538055":7.6,"2.606547":7.7,"2.60425":7.8,"2.673762":7.9,"2.706445":8,"2.708914":8.1,"2.739847":8.2,"2.773871":8.3,"2.831112":8.4}');
       insert into Lookup values (NULL, 2,'Lookup for 12.6V circuit', 1, 2, 1,15, '{"2.313196":9.6,"2.337292":9.7,"2.386696":9.9,"2.40958":10.0,"2.433717":10.1,"2.457771":10.2,"2.481867":10.3,"2.506913":10.4,"2.530059":10.5,"2.554154":10.6,"2.579713":10.7,"2.602822":10.8,"2.626441":10.9,"2.652024":11.0,"2.674633":11.1,"2.698729":11.2,"2.722825":11.3,"2.746921":11.4,"2.771016":11.5,"2.795112":11.6,"2.819208":11.7,"2.843304":11.8,"2.867399":11.9,"2.891496":12.0,"2.915591":12.1,"2.939687":12.2,"2.961373":12.3,"2.987879":12.4,"3.011974":12.5,"3.03607":12.6}');

Application:
                             # (id integer primary key, app_id integer, desc varchar, owner_id integer, circuit_id integer, mosfet_id integer);
       insert into Application values(NULL,1,'Application to build the software',1 )

Application JOIN tables: config, application, owner, circuit, tempc, using the where clause...
         select * from Application as a join owner as o where a.owner_id= o.owner_id;
          select c.app_id, c.version, c.timestamp, a.desc, o.name, t.tempc , crc.desc, crc.r1,crc.r2, crc.rp, crc.rg from Application as a, Owner as o, TempC as t, Config as c,
   ...>            Circuit as crc  where c.app_id=a.app_id and a.owner_id=o.owner_id and c.tempc_id=t.tempc_id and crc.app_id=a.app_id order by crc.circ_id;

Config
       CREATE TABLE Config( id integer primary key, config_id integer, version integer, owner_id integer, app_id integer, tempc real);
       iinsert into config values (NULL, 1, 1, 'Baseline configuration',1746154268, 1, 1,0,2, 14);

Runtime :
RT+Config:
      	CREATE TABLE RT_CONFIG (ID INTEGER PRIMARY KEY , RTCFG_ID INTEGER NOT NULL, VERSION_ID INTEGER NOT NULL, VERSION_DESC VARCHAR, CHANNEL_DESC VARCHAR, TIMESTAMP INTEGER,  TEMPC REAL, MOSFET_ID INTEGER, MOSFET_TYPE VARCHAR, R1 REAL, R2 REAL, RP REAL, RG REAL, LUT VARCHAR);
     INSERT into RT_CONFIG values (NULL,0,'4.2V channel(0)', 1, 'Baseline',   1746223938,25.7,1,'P-CHANNEL',1000.0,329.6,10000.0,331.2,'{}');
     INSERT into RT_CONFIG values (NULL,1,'first rt config',   '8.4 V channel(1)', 1746223938,25.7,2,'P-CHANNEL',1002.5,503.0 ,10003.0,476.0,'{}');
     INSERT into RT_CONFIG values(NULL,2,first rt config',    '12.6 V channel(2)',1746223938,25.7,3,'P-CHANNEL',1007.0,336.0,10003.0,476.0,'{}');
     SELECT * FROM RT_CONFIG;
Timestamp: date +%s; cast as integer (done in a command prompt or terminal
g
