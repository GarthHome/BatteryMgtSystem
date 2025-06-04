#Based on data base file: /Users/garth/Programming/MicroPython/usb/ryan/voltage_divider/data/rt_db

select * from rt_config where owner='GM' and channel_id=0 and app_id=1 and version_id=1;
select * from rt_config where owner='GM' and channel_id=1 and app_id=1 and version_id=1;
select * from rt_config where owner='GM' and channel_id=2 and app_id=1 and version_id=1;

DROP TABLE RT_CONFIG;

CREATE TABLE RT_CONFIG (ID INTEGER PRIMARY KEY , owner varchar, app_id integer, app_desc varchar, channel_id integer, CHANNEL_DESC VARCHAR , VERSION_ID INTEGER NOT NULL, VERSION_DESC VARCHAR,  TIMESTAMP INTEGER,  MOSFET_ID INTEGER, MOSFET_TYPE VARCHAR, TEMPC REAL, R1 REAL, R2 REAL, RP REAL, RG REAL, CALIBRATED integer , LUT VARCHAR);
 

# All of the following will need to be calibrated ...

#channel 0 insert

insert into rt_config values(NULL,'GM',1,'Development', 0,'4.2V CIRCUIT CHANNEL(0)',1,'BASELINE VERSION',1746656778,1,'P-CHANNEL',25.4,330.0,1000.0,10000.0,220.0,0,'{"2.196316":3.0,"2.269526":3.1,"2.342736":3.2,"2.415946":3.3,"2.489157":3.4,"2.562367":3.5,"2.635578":3.6,"2.708788":3.7,"2.781999":3.8,"2.855209":3.9,"2.92842":4.0,"3.00163":4.1,"3.07484":4.2,"3.14805":4.3,"3.22126":4.4,"3.29447":4.5}');



#channel 1 insert

insert into rt_config values(NULL,'GM',1,'Development',1,'8.4V CIRCUIT CHANNEL(1)',1,'BASELINE VERSION',1746656778,2,'P-CHANNEL',25.4,1000.0,510.0,10000.0,480.0,0,'{2.02278: 6.0, 2.058313: 6.1, 2.093844: 6.2, 2.129375: 6.3, 2.164906: 6.4, 2.197645: 6.5, 2.23: 6.6, 2.230969: 6.7, 2.26361: 6.8, 2.298156: 6.9, 2.364712: 7, 2.402375: 7.1, 2.435156: 7.2, 2.4688: 7.3, 2.466984: 7.4, 2.503416: 7.5, 2.538055: 7.6, 2.60425: 7.8, 2.606547: 7.7, 2.673762: 7.9, 2.706445: 8, 2.708914: 8.1, 2.739847: 8.2, 2.773871: 8.3, 2.831112: 8.4, 2.866643: 8.5, 2.902174: 8.6, 2.93770: 8.7, 2.973236: 8.8, 3.008767: 8.9, 3.044298: 9.0}');

#channel 2 insert

insert into rt_config values(NULL,'GM',1,'Development',2,'12.6V CIRCUIT CHANNEL(2)',1,'BASELINE VERSION',1746656778,3,'P-CHANNEL',25.4,1000.0,330.0,10000.0,480.0,0, '{2.16861: 9.0, 2.192715: 9.1, 2.216811: 9.2, 2.240907: 9.3, 2.265004: 9.4, 2.2891: 9.5, 2.313196: 9.6, 2.337292: 9.7, 2.386696: 9.9, 2.40958: 10.0, 2.433717: 10.1, 2.457771: 10.2, 2.481867: 10.3, 2.506913: 10.4, 2.530059: 10.5, 2.554154: 10.6, 2.579713: 10.7, 2.602822: 10.8, 2.626441: 10.9, 2.652024: 11.0, 2.674633: 11.1, 2.698729: 11.2, 2.722825: 11.3, 2.746921: 11.4, 2.771016: 11.5, 2.795112: 11.6, 2.819208: 11.7, 2.843304: 11.8, 2.867399: 11.9, 2.891496: 12.0, 2.915591: 12.1, 2.939687: 12.2,     2.961373: 12.3, 2.987879: 12.4, 3.011974: 12.5, 3.03607: 12.6, 3.060166: 12.7, 3.084262: 12.8, 3.108358: 12.9, 3.132454: 13.0, 3.15655: 13.1, 3.180646: 13.2, 3.204742: 13.3, 3.228838: 13.4, 3.252934: 13.5}');


# for Ryan Pullen:
insert into rt_config values(NULL,'RP',1,'Dog Backpack', 0,'4.2V CIRCUIT CHANNEL(0)',1,'BASELINE VERSION',1746656778,1,'P-CHANNEL',25.4,330.0,1000.0,10000.0,220.0,0,'{}');

insert into rt_config values(NULL,'RP',1,'Dog Backpack',1,'8.4V CIRCUIT CHANNEL(1)',1,'BASELINE VERSION',1746656778,2,'P-CHANNEL',25.4,1000.0,510.0,10000.0,480.0,0,'{}');

insert into rt_config values(NULL,'RP',1,'Dog Backpack',2,'12.6V CIRCUIT CHANNEL(2)',1,'BASELINE VERSION',1746656778,3,'P-CHANNEL',25.4,1000.0,330.0,10000.0,480.0,0, '{}');

update rt_config set LUT='{2.111:3.0, 2.222:3.1....}' where owner ='RP' and app_id=1 and channel_id=0 and version_id=1;
...
