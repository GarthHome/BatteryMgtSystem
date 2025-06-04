#file: testMosfet.py
import sys

from machine import  Pin, PWM
import time

#PWM(2,freq =1,duty=512)    
print(sys.implementation)
p2=Pin(2, Pin.OUT)

#TODO: Find out why the Esp32 cannot trigger the Mosfet. Signal too weak????I can get Mosfet to switch if I apply 4.2 Volts or ground the gate lead thru Rg.

# Mosfet Testing.  PWM (27, freq=16, duty=512) . Gate resistor must limit current < 20 mA
# 1. Mosfet turns on when p27 goes LOW. (vgs< - 4V.)
# 2. Drain voltage is constant over  ON  time. ( ~31.25 MS)
#3. Ensure that at least 3 A of current flows  when on. (30A promised)
# 4. Ensure that the Vgs < 2 - 4 V.  (  10k & 330Ω results in -5.5 Vgs)

# 3 seconds on, 3 seconds off. Use this to ensure that Mosfet turns on and off when it should.
while True:
    p2.on()
    print(p2.value())
    time.sleep (3)
    p2.off()
    print(p2.value())
    time.sleep(3)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    