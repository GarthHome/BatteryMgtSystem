#file: rpvdclass.py


from rpvd_config import  names, gates,  _BUFFERSIZE,  ADCC, Measurements, Record, Stats, measurements 
from machine import Pin, RTC, SoftI2C, PWM, Timer
import ads1x15
from time import ticks_us, ticks_diff, ticks_ms, localtime
import math
import sys
up = sys.implementation.name == "micropython"
import asyncio


async def circuit(r, i):  # Coro to await
    print(r, i)
    await r.measure(i)
    await asyncio.sleep(1)
    return i


circs=["C42","C84","C126", "Timer"]
# nemonics for circuits and modes
C42=0
C84=1
C126=2
CALIBRATE=1            #mode
MEASURE=0            #mode
_BUFFERSIZE=_BUFFERSIZE
#globals
rec=-1
#i2c and sampler 
i2c= SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
ads=ads1x15.ADS1115(i2c, ADCC.addr, ADCC.gain)    # ADC sampler


class rpvd:
    def __init__(self):
        #init()   # fill in fields in the config file...
        self.names=names
        self.gates=gates
        self.measurements= measurements
        self.stats=-1           #named tuple Stats is populated in compute_stats.
        self.irq_pin = Pin(17, Pin.IN, Pin.PULL_UP)   
        self.index_put=0 
        self.dur  =-1                                                     
        self.realtime=0                                                 
        self.mode = MEASURE                                                  
        self.channel=-99                                             
        self.rtc=RTC()                      #rtc us realtime clock, which furnishes datetimestamp for files.
        self.check_i2c()
        self.__str__()
        self.vin=-1                         #set in calibrate
        self.wait_period=60
        
    async def __await__(self):
        '''Measure all three channels in order, then sleep for waitTime ( hour), then repeat for ever...'''
        while True:
            for n in range(4):
                print(f'__await__measure  {circs[n]} called')
                if n == 3:
                    t= localtime()
                    print(f"--------------{t}-------------------")
                    await asyncio.sleep(self.wait_period)     #hourly
        return res
        
    def __str__(self):
         print("r attributes: ", self.__dict__.keys())
         
    def check_i2c(self):
        '''if ADS1115 ADDR pin is grounded, should return 72'''
        if i2c.scan()[0] == 72:
            print("i2c is working...")
        else:
            print("I2c is not working. Troubleshoot connections")
    
    # IRQ method triggered by ADC ALRT pin when ADS is ready for sample to be read.
    def sample_auto(self, x, adc = ads.alert_read ):
        '''Sets storage arrays depending on the active channel , measures storage time. The storage time must be less than 1/sample_rate.'''
        data=self.data()
        timestamp=self.timestamp()
        strt = ticks_us()                                                                #can remove when realtime load is known.
        if self.index_put < _BUFFERSIZE:
            data[self.index_put] = adc()
            timestamp[self.index_put] = ticks_us()
            secs= ticks_diff(ticks_us() , strt) /1e6   #measured in µs, convert to secs.
            self.realtime=max(secs, self.realtime)  # stores the longest time needed to read, store data, timestamp over the _BUFFERSIZE samples
            self.index_put += 1
            
    def datetimestamp(self):
        dt = self.rtc.datetime()
        return f'{dt[0]}-{dt[1]}-{dt[2]}  {dt[4]}:{dt[5]}:{dt[6]}.{dt[7]}'
    
#     def start_pwm(self, channel):
#         '''Sets the designated pin to broadcast PwM signal. Used for OScope viewing of gate transitions'''
#         self.channel=channel
#         #PWM(Pin(x), freq=16, duty=512)   # run in Shell. Pin(x) will emit a pwm signal. Used to see transitions in OScope.
#         
#     
#     def stop_pwm(self):
#         PWM(self.gates[self.channel],freq=1, duty=0)
#         
    def turn_on(self, chn):
         '''Setting the gate pin to LOW drains the Mosfet Gate Capacitor so Vgs goes negative. When Vgs < -2V, Mosfet conducts with full current.'''
         self.gates[chn].off()
         self.show_gates()
         
    def turn_off(self, chn):
        '''Setting gate pin to HIGH allows pullup resistor to charge Mosfet Capacitor, turning off current.'''
        self.gates[chn].on()
        self.show_gates()
        
    def show_gates(self):
        print(self.gates[0], self.gates[1],self.gates[2])
        print((self.gates[0].value(), self.gates[1].value(), self.gates[2].value())) 


    def measure(self, ch, vin=-1):
        ''' Prepares circuits[ch] to turn on current and sample voltages at the sample point between r1 and r2. If mode==MODE_PWM the MOSFET will
        turn on and off repeatedly at freq. This allows one to see the transition times for turn on and turn off on the OScope. The sampled a2d values
        may be low if wait time is not enough.. For OScope, show two channels: Green for gate voltage and Yellow for sample Voltages.'''
        self.vin=vin
        self.channel = ch
        gate_open=ticks_us()
        self.turn_on(ch)
        #self.circuit = self.circuits[ch]
        self.meas = self.measurements[ch]
        #add handler for irq
        self.irq_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.sample_auto) 
        ads.conversion_start(ADCC.sample_rate, self.channel)  #if channel==0 the a2d values will come from A0, if 1 then A1, if 2 then A2
        print(" Wait for samples...", _BUFFERSIZE)
        while self.index_put < _BUFFERSIZE:
            pass
        print("Done...A2D samples should be in self.measurements[self.channel].data")
        self.turn_off(self.channel)
        # time from gate_open until gate_close in µs converted to seconds
        secs= ticks_diff(ticks_us(), gate_open )/ 1e6
        #print(" sampling secs: ", secs)
        self.dur= secs
        
        dsum = sum(self.meas.data)
        print("Sum of data array: ", dsum)
        if  dsum > 0:
            if self.mode == CALIBRATE:
                self.compute_volts()
                volts=self.volts()
                mean=sum(volts)/len(volts)
                return mean
            self.process()
            self.index_put=0
        else:
            print('No data. exiting...')
            self.index_put=0 
            return
    def measurement(self):
        return self.measurements[self.channel]
    
    def data(self):
        return self.measurements[self.channel].data
    
    def timestamp(self):
        return self.measurements[self.channel].timestamp
    
    def realtime(self):
        return self.measurements[self.channel].realtime
    
    def volts(self):
        return self.measurements[self.channel].volts
    
    def vars(self):
        return self.measurements[self.channel].vars
    
    def compute_volts(self):
        '''converts each a2d count in data to volts and stores it in volts array'''
        # get access to the arrays for conversion and storage.
        volts = self.volts()
        data=self.data()
        #convert each a2d count to voltage and store it in volts array
        for i in range(len(data)):
            volts[i] = ads.raw_to_v( data[i] )
            
    def process(self):
        '''Computes/stores volts , vars, stats, battery_level. Creates csv record and stores it on the device in /data/...'''
        (m,sd,snr) = self.compute_stats(self.measurements[self.channel].data)  # on adc values
        keep = self.reject_outliers(m,sd)
        (m,sd,snr) = self.compute_stats(keep)
        vm = ads.raw_to_v(m)   # multiply a2d by LSB=122µv 
        sd = ads.raw_tov(sd)
        snr=m/sd
        vb = self.lookup_vb(vm)
        level = self.get_battery_level(vb)
        dur=self.dur
        circuit_name = self.names[self.channel]
        print("circuit: ", circuit_name, "vm: ", vm, "sd: ", sd, "snr: " , snr, "vb: ", vb, "level: ", level)
        # self.create_record()
        
    def get_battery_level(self, vb):
        charged = self.circuits[self.channel].VH
        discharged = self.circuits[self.channel].VL
        percent = round( (vb -discharged) / (charged - discharged) * 100 , 2)
        return percent
    
    def get_status(self, vm):
        '''Gets lower bound and upper bound from LUT for this channel. if   low < vm < hi: OK else show action needed.'''
        low= self.lut[self.channel][0][0]  #first pair.vm
        hi = self.lut[self.channel][-1][0]   #last pair.vm
        stat=' '
        if vm < low:
            stat= 'Needs Recharge'
        elif vm > hi:
            stat='Over charged'
        else:
            stat= 'OK'
        return stat
                                        
                        
    def compute_stats(self, samples):
        '''Compute mean, sd, snr  of a2d values. '''
        vars = []
        mean = sum(samples)/len(samples)
        for i in range(len(samples)):
            d=samples[i] - mean
            vars.append(d*d)
        var=sum(vars)/len(vars)
        sd=math.sqrt(var)
        snr=mean/sd      
        print("sample mean: ", mean)
        print("sample std deviation: ", sd)
        print("Sample Signal to Noise Ratio: ", snr)
        return (mean, sd, snr)
       
   
        dur=self.dur
        circuit_name = self.names[self.channel]
        #Stats = namedtuple("Stats", ("circuit_name", "dur", "mean", "sd", "snr","vb", "diff", "level", "status"))   #9 fields
        diff= self.vin - vb
        self.stats= Stats(circuit_name, dur, mean, sd, snr, vb, diff, level, self.get_status(mean))

    def record_header(self):
        return f'datetime,                            circuit,  bat,    Vin,    r1,    r2,     vm,            vm_sd,             vm_snr,      Vb,           amps,           ts,      level,     error'
   
    def create_record(self):
        global rec
        ''' Create and stores a record on disk to reflect measurements...'''
        aCircuit=self.circuits[self.channel]
        dts=self.datetimestamp()
        circuit_name = names[self.channel]
        v_tap=aCircuit.VH
        r1=aCircuit.r1
        r2=aCircuit.r2
        fract = aCircuit.fract
        vm= self.stats.mean
        vm_sd= self.stats.sd
        vm_snr=self.stats.snr
        #Vb= vm/fract  + adj   # replaced fract method with equation for range    2.326281 < vm < 3.050727 on 12.4 V Circuit. Need to see if other Circuits agree...
        Vb= self.lookup_vb(vm)
        amps=Vb/r2
        ts= self.dur
        watts = amps * (r1+r2)
        amp_secs=ts*amps
        watt_secs=ts*watts
        batt_level = self.get_battery_level(Vb)
        #user enters the Vin voltage, used for lookup file and rec file
        
#         pct_err = (self.vin-Vb)/self.vin * 100
#         pe = f'{pct_err }%'
        #print( pe)
        #TODO Find out why Record has 16 fields here when it has 14 fields in the rpvd_config, which is imported. 
        #TODO-DONE: Both class and config file must be on the device to keep them in sync.
        error = self.vin-Vb
        rec = Record(dts, circuit_name, v_tap, self.vin,  r1, r2, vm, vm_sd, vm_snr, Vb, amps, ts, batt_level ,error)
        print("Record: ", rec)
        self.store_rec(rec)
      
            
        
    def store_rec(self, record):
        '''Measuring, writes a multi-column record to a csv file on the device in folder.data'''
        name = names[self.channel]
        filename = f'{DATAPATH}/{name}.csv'
        print ("path: ", filename)
        line = str(tuple(record))[1:-1]      
        index=-1   
        #check for header
        with open(filename,'a') as csvfile:
            s= csvfile.read(9)
            print("s: ", s)
            index = s.find('datetime,')
            csvfile.close()            
        #open csv file in append/text mode .  if header is absent write it first
        print("filename: ", filename)
        with open(filename, "a") as csvfile:
            if index == -1:
                csvfile.write(self.record_header())
            csvfile.write('\n'+line)
            csvfile.close()
     
    def show_lookup(self, chan):
        print("Channel: ", chan, "  LUT", self.lut[chan])
        name=self.names[self.channel]
        filename= f'{DATAPATH}/{name}.LUT'
        print("filename: ", filename)
        with open(filename ) as lutfile:
            data = lutfile.read()
            print(data)
            lutfile.close()
          
    def show_file(self, chan):
        name=self.names[chan]
        filename= f'{DATAPATH}/{name}.csv'
        print("filename: ", filename)
        with open(filename) as csvfile:
            data = csvfile.read()
            print(data)
            csvfile.close()
          
    def lookup_vb(self, vm):
        ''' If vm is too small or too large for lut, prints warning and returns, else, Finds pairs in lut which surround vm, then interpolates to estimate vb.'''
#         alut = self.lut[self.channel]
#         print("alut: ", alut)
#      
#         #since luts ( pairs) are arranged in ascending order , step from first to last . every pair's vm will replace lw until the next vm is larger.
#         Bracket is complete, call interpolate with bracketing vms and input vm.
#         lw=(0,0)
#         for p in alut:   #p stands for pair  (vm,vb)
#             if p[0] > vm:
#                 print((lw, vm, p ))
#                 vb= self.interpolate(vm,p,lw)
#                 out=f"Lookup of: {vm} yields: {vb}"
#                 print(out)
#                 break
#             else:
#                 lw=p
#                 vb= -99
        slope = self.line_parms[self.channel].slope
        bias = self.line_parms[self.channel].bias
        vb = vm *slope +bias
        return vb 
    
                
    def interpolate(self, vm, hr, lw):
       '''Assumes linearity between sample points, so interpolation should suffice'''
       rngx = hr[0]-lw[0]
       rngy = hr[1]-lw[1]
       pctx= (vm-lw[0])/rngx
       #print(rngx, rngy, pctx)
       valy= pctx * rngy +lw[1]
       #print("Vb: ", valy)
       return valy
  
                
    def calibrate(self, vb, channel, runs):
        ''' The mean vm will be used to set values for vm in lookup table. Output can be copied and pasted into rpvd_config.lut[channel]'''
        vms=[]
        self.channel=channel
        self.mode=CALIBRATE
        self.vin=vb
        volts=self.volts()
        for i in range(runs):
            r.turn_on(channel)
            vms.append(r.measure(channel,vb))
            
        print("vms: ", vms)
        mean = sum(vms)/len(vms)
        new_tup =( mean, vb)                # mean of vms but same vb
        #find index of the tuple with vb in it
        lut=r.lut[r.channel]
        ndx=[i for i in range(len(lut)) if lut[i][1]==vb][0]
        print("old tup: ", lut[ndx])
        lut[ndx]= new_tup
        print("new tup: " ,lut[ndx])
        filename=f'{DATAPATH}/{self.names[self.channel]}.LUT '
        with open(filename, "w") as lutfile:
            lutfile.write(str(r.lut[r.channel]))
            lutfile.close()
        
        #TODO: DONE actually write the calibration tuple into the LUT in memory.   User should copy from memory and paste it into the config file.      
                    
    def reject_outliers(self, mean, sd):
        '''Throw away any samples outside of mean +3sd'''
        samples= self.data
        sd3=3*sd
        keep = [ s  for s in samples if (abs(s-m) < sd3) ]
        sts=self.stats
        sd3=3*sts.sd
        m=sts.mean
     #TODO : Done. method reject_outliers()  is completely done. Already have stats , no need to compute them again. just use stats to set limit for rejection
        keep = [ v  for v in vlts if (abs(v-m) < sd3) ]
        out=  [ v  for v in vlts if (abs(v-m) > sd3) ]
        #  if any outliers, now using keep compute m,sd,sd3 again, otherwise, no further action
        if len(out) > 0:
            m=sum(keep)/len(keep)
            vars=[ (m-v)**2 for v in keep]
            sd = math.sqrt( sum(vars)/len(vars))
            sd3 = 3* sd
            print("2ndPass: mean: ", m, " sd: :", sd, " sd3: ", sd3)
            vb=self.lookup_vb(m)
            if self.vin > 0:
                diff = self.vin-m
            else:
                diff=-1
            st=self.stats
            print("pre stats", st)
            circ_name = self.names[self.channel]
            # Stats = namedtuple("Stats", ("circuit_name", "dur", "mean", "sd", "snr","vb", "level", "status"))                                                                                            #8 fields
            self.stats=Stats(circ_name, st.dur, sts.mean,sts.sd,  m/sts.sd, vb, diff, st.level, st.status )
            print("post-stats", self.stats )  
      
            #TODO: Figure out how to use timer to run the measure(...) method. rpvd is stopping as soon as it tells user to wait for 32 samples
            #TODO: Fix the wiring on C126 so that green lead grounds the gate.
    __iter__ = __await__
  

async def setup_tasks():
    r= rpvd()  #rpvd is awaitable
    print('waiting for rpvd')
    r.wait_period=3600 # seconds - 1 hour
    res = await rpvd()  # Retrieve voltages
    print('done', res)

# Run this from the shell:         asyncio.run(setup_tasks())class.py
