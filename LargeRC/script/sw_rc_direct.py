# -*- coding: utf-8 -*-
import visa

from mpy.device.driver import DRIVER
from mpy.tools.Configuration import strbool
from mpy.tools.Configuration import fstrcmp
from mpy.tools.util import format_block


class SWController(DRIVER):
    conftmpl={'description': 
                 {'description': str,
                  'type': str,
                  'vendor': str,
                  'serialnr': str,
                  'deviceid': str,
                  'driver': str,
                  'class': str},
                'init_value':
                    {'fstart': float,
                     'fstop': float,
                     'fstep': float,
                     'gpib': int,
                     'output': str,
                     'swfreq': float,
                     'virtual': strbool}}

    def __init__(self):
        self.LF='R1P0R2P1R3P1R6P0'
        self.HF='R1P0R2P2R3P0R6P1'
        self.term_chars = visa.LF
        DRIVER.__init__(self)
        self.error=0
        self.islf=None
    
    def ask(self, cmd):
        if not self.dev:
            return None
        ans=self.dev.ask(cmd)
        return ans
    
    def Init(self, ini, ch=1):
        self.error=DRIVER.Init(self, ini, ch)

        self.out='powermeter'
        try:
            self.out = self.conf['init_value']['output']
            self.out = fstrcmp(self.out,('receiver','powermeter'), n=1, cutoff=0, ignorecase=True)[0]
        except KeyError:
            pass
        
        self.swfreq=1e9
        try:
            self.swfreq = self.conf['init_value']['swfreq']
        except KeyError:
            pass
        return self.error

    def _islf(self):
        ans = self.ask('')
        R3=self.LF[self.LF.index('R3'):self.LF.index('R3')+4]
        R6=self.LF[self.LF.index('R6'):self.LF.index('R6')+4]
        return (R3 in ans) and (R6 in ans)
        
    def SetFreq(self, f):
        if f<=self.swfreq:
            cmd=self.LF
        else:
            cmd=self.HF
        ans=self.ask(cmd)
        self.SetAtt(False)
        return 0, f

    def SetAtt(self, state=True):
        pm=(self.out == 'powermeter')
        if self._islf():
            if state:  #  Att on
                if pm:
                    cmd='R4P1R5P0'  # pm, lf, 20 dB
                else:
                    cmd='R4P0R5P0'  # rec, lf, 20 dB              
            else:       # Att off
                if pm:
                    cmd='R4P0R5P1'   # pm , lf, 0 dB                
                else:
                    cmd='R4P1R5P1'   # rec, lf, 0 dB             
        else:   
            if state:  # Att on
                if pm:
                    cmd='R4P1R5P1' # pm, hf, 20 dB
                else:
                    cmd='R4P0R5P1' # rec, hf, 20dB               
            else:
                if pm:             
                    cmd='R4P0R5P0' # pm, hf, 0 dB               
                else:
                    cmd='R4P1R5P0'  # rec, hf, 0 dB
        #print state, pm, cmd
        ans=self.ask(cmd)
        return ans
        
    def Quit(self):
        return 0

if __name__ == '__main__':
    import io
    import numpy as np
    import time

    ini=format_block("""
                    [DESCRIPTION]
                    DESCRIPTION = RC RX Switch
                    TYPE = Custom
                    VENDOR = 
                    SERIALNR = 
                    DEVICEID = 
                    DRIVER = sw_rc_direct
                    CLASS = SWController

                    [INIT_VALUE]
                    FSTART = 0
                    FSTOP = 18e9
                    FSTEP = 0.0
                    GPIB = 2
                    OUTPUT = RECEIVER
                    SWFREQ = 1e9
                    VIRTUAL = 0
                    """)
    ini=io.StringIO(ini)
    
    sw=SWController()
    sw.Init(ini)
    for f in np.linspace(0,4.2e9,10):
        print(f, sw.SetFreq(f))
        print("Att On: ", sw.SetAtt()) 
        time.sleep(1)
        print("Att Off:", sw.SetAtt(False)) 
        time.sleep(1)

    sw.Quit()