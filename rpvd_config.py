#file: rpvd_config.py

'''Contains the namedtuples that describe each circuit. Contains each circuit values. '''

from collections import namedtuple
from array import array
from machine import Pin, PWM
import micropython

# rds_on =  0.07   # MosFet resistance when on.. From MosFet Datasheet. Not used since lut was introduced.
PATH = '//Users/garth/Programming/MicroPython/scripts/rpvdclass.py'

names = ["C42", "C84", "C126"]
C42=micropython.const(0)
C84=micropython.const(1)
C126=micropython.const(2)

gate_42=Pin(25, Pin.OUT, Pin.PULL_UP)
gate_84=Pin(26, Pin.OUT, Pin.PULL_UP)
gate_126=Pin(27, Pin.OUT, Pin.PULL_UP)

gates = [gate_42, gate_84, gate_126]
                                                
#namedtuples
#Circuit = namedtuple("Circuit", ("circuit_name", "VH", "VL", "r1", "r2", "fract",  "vm_max", "amps_max", "powr_max", "circ_powr"))                                          # 10fields
Measurements = namedtuple("Measurements",("circuit_name", "data", "timestamp"))                                                                                        #5 fields
Stats = namedtuple("Stats", ("circuit_name", "dur", "mean", "sd", "snr","vb", "diff", "level", "status"))                                                                                           #9 fields
Record = namedtuple("Record", ("datetime", "circuit_name",  "v_tap","V_in", "r1","r2","vm", "vm_sd", "vm_snr", "Vb", "amps", "ts",  "level", "err")  )            # 14 fields
Timing = namedtuple("Timing", ("Period_ms","processing_sec"))
ADC= namedtuple("ADC", ('addr',"sample_rate","sample_size","gain"))
GatePins = namedtuple("GatePins",("C_42", "C_84", "C_126"))

ADCC=ADC(72, 3, 64, 1)    # ADC config
_BUFFERSIZE = micropython.const(64)

timing= Timing(60000, 3)      # hourly = 60*60 *1000 ms = 3600e3,   @32 sps/circuit => 1 sec/circuit * 3 circuits plus time to convert a2d to voltage etc.

# data types for arrays are found in: https://docs.micropython.org/en/latest/library/array.html
# and https://docs.micropython.org/en/latest/library/struct.html#module-struct. Problems may require changing real nums from d to type 'f' (smaller)
#build following arrays for each channel: data, timestamp

data42 = array("h", (0 for _ in range(_BUFFERSIZE)))
data84 = array("h", (0 for _ in range(_BUFFERSIZE)))
data126 = array("h", (0 for _ in range(_BUFFERSIZE)))
timestamp42 = array("L", (0 for _ in range(_BUFFERSIZE)))
timestamp84 = array("L", (0 for _ in range(_BUFFERSIZE)))
timestamp126 = array("L", (0 for _ in range(_BUFFERSIZE)))

meas42= Measurements(names[0], data42, timestamp42)
meas84= Measurements(names[1], data84, timestamp84)
meas126 = Measurements(names[2], data126, timestamp126)
 
measurements= [meas42, meas84, meas126]

   #  from rpvd_config import  timing,  Record , Timing,  ADCC, lut
   
        