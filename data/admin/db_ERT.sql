CREATE TABLE TempC (id integer primary key, tempc_id integer, tempc real);
CREATE TABLE owner( id integer primary key, owner_id integer, name varchar);
CREATE TABLE datasheets( id integer primary key, device_id, desc varchar,  url varchar );
CREATE TABLE circuit( id integer primary key, circ_id integer, app_id integer, version integer, desc varchar, mosfet_id INTEGER, R1 REAL, R2 REAL, RP REAL, RG REAL,  B_CELL_1 INTEGER, B_CELL_2 integer, B_CELL_3 integer);
CREATE TABLE mosfet (id integer primary key, mosfet_id integer, rise_time real, fall_time real, overshoot_rise  real, overshoot_fall);
CREATE TABLE Application (id integer primary key, app_id integer, desc varchar, owner_id integer );
CREATE TABLE Config( id integer primary key, config_id integer, version integer, timestamp integer, owner_id integer, app_id integer, tempc_id);
CREATE TABLE Lookup (id integer primary key, lut_id integer, lut_desc varchar, app_id integer, circuit_id integer, mosfet_id integer, tempc_id integer, lut varchar);


Config : config_id, version, reason_verson, timestamp, owner_id, app_id, tempc_id, mosfet_id, lookup_id, 

TempC.tempC_id, TempC.tempc 
Owner.owner_id, Owner.name
Circuit : circ_id,  r1, rp, rg, version
Application: app_id, desc, owner_id, 
Lookup : lut_id, lut_desc, app_id, circuit_id, mosfet_id,tempc_id, lut

Abbreviations for Table Names:
Config      as cfg
TempC       as temp
Owner       as own
Circuit     as crct
Application as app
Lookup      as look
Mosfet      as msft


where clauses:
cfg.app_id = app.app_id
cfg.tempc_id = temp.tempc_id
cfg.owner_id = own.owner_id
cfg.circuit_id crct.circuit_id
cfg.lookup_id = look.lukup_id
cfg.mosfet_id = msft.mosfet_id

