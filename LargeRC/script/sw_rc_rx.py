# -*- coding: utf-8 -*-
from mpy.device.driver import DRIVER
from mpy.tools.Configuration import strbool
from mpy.tools.Configuration import fstrcmp
from mpy.tools.util import format_block

LF='R3P1R6P0'
HF='R3P0R6P1'

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
        self.islf=(LF in self.ask(''))
        return self.error
        
    def SetFreq(self, f):
        if f<self.swfreq:
            cmd=LF
        else:
            cmd=HF
        ans=self.ask(cmd)
        self.islf=(LF in ans)
        return 0, f

    def SetAtt(self, state=True):
        pm=(self.out == 'powermeter')
        if self.islf:
            if state:
                if pm:
                    cmd='R4P1R5P0'
                else:
                    cmd='R4P0R5P0'                
            else:
                if pm:
                    cmd='R4P0R5P1'                
                else:
                    cmd='R4P1R5P1'                
        else:
            if state:
                if pm:
                    cmd='R4P1R5P1'
                else:
                    cmd='R4P0R5P1'                
            else:
                if pm:
                    cmd='R4P0R5P0'                
                else:
                    cmd='R4P1R5P0'                        
        ans=self.ask(cmd)
        return ans
        
    def Quit(self):
        return 0

if __name__ == '__main__':
    import StringIO
    import numpy as np
    import time

    ini=format_block("""
                    [DESCRIPTION]
                    DESCRIPTION = RC RX Switch
                    TYPE = Custom
                    VENDOR = 
                    SERIALNR = 
                    DEVICEID = 
                    DRIVER = sw_rc_rx
                    CLASS = SWController

                    [INIT_VALUE]
                    FSTART = 0
                    FSTOP = 18e9
                    FSTEP = 0.0
                    GPIB = 2
                    OUTPUT = POWERMETER
                    SWFREQ = 1e9
                    VIRTUAL = 0
                    """)
    ini=StringIO.StringIO(ini)
    
    sw=SWController()
    sw.Init(ini)
    for f in np.linspace(0,4.2e9,20):
        print f, sw.SetFreq(f)
        print "Att On:", sw.SetAtt() 
        time.sleep(0.5)
        print "Att Off:", sw.SetAtt(False) 

    sw.Quit()