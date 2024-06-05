# -*- coding: utf-8 -*-
# import pyvisa

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
        self.r1_LF = 'R1P1'
        self.r1_HF = 'R1P2'
        self.r1_DIRECT = 'R1P4'
        self.r2_TERM = 'R2P0'
        self.r2_GTEM = 'R2P1'
        self.r34_REST = 'R3P1R4P0'  # RX TERM and RX LF input
        self.LF = None
        self.HF = None

        self.term_chars = '\n'   # visa.LF
        DRIVER.__init__(self)
        self.error = 0
    
    def query(self, cmd):
        if not self.dev:
            return None
        ans = self.dev.query(cmd)
        return ans
    
    def Init(self, ini, ch=1):
        self.error=DRIVER.Init(self, ini, ch)
        
        # self.ask('R1P4R2P0R3P1R4P0') # save settings

        self.out = 'term'
        try:
            self.out = self.conf['init_value']['output']
            self.out = fstrcmp(self.out, ('term', 'gtem'), n=1, cutoff=0, ignorecase=True)[0]
        except KeyError:
            pass
        if self.out == 'gtem':
            self.LF = self.r1_LF + self.r2_GTEM
            self.HF = self.r1_HF + self.r2_GTEM
        else:
            self.LF = self.r1_LF + self.r2_TERM
            self.HF = self.r1_HF + self.r2_TERM

        self.swfreq=1e9
        try:
            self.swfreq = self.conf['init_value']['swfreq']
        except KeyError:
            pass
        return self.error
        
    def SetFreq(self, f):
        if f <= self.swfreq:
            cmd = self.LF+self.r34_REST
        else:
            cmd = self.HF+self.r34_REST
        ans = self.query(cmd)
        return 0, f

    def Quit(self):
        return 0

if __name__ == '__main__':
    import io
    import numpy as np
    import time

    ini=format_block("""
                    [DESCRIPTION]
                    DESCRIPTION = GTEM Switch
                    TYPE = Custom
                    VENDOR = 
                    SERIALNR = 
                    DEVICEID = 
                    DRIVER = sw_gtem
                    CLASS = SWController

                    [INIT_VALUE]
                    FSTART = 0
                    FSTOP = 18e9
                    FSTEP = 0.0
                    GPIB = 8
                    OUTPUT = GTEM
                    SWFREQ = 1e9
                    VIRTUAL = 0
                    """)
    ini = io.StringIO(ini)
    
    sw = SWController()
    sw.Init(ini)
    for f in np.linspace(0, 4.2e9, 10):
        print(f, sw.SetFreq(f))
        time.sleep(1)

    sw.Quit()