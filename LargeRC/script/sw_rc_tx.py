# -*- coding: utf-8 -*-
# import pyvisa

from mpy.device.driver import DRIVER
from mpy.tools.Configuration import strbool
from mpy.tools.Configuration import fstrcmp
from mpy.tools.util import format_block


class SWController(DRIVER):
    conftmpl = {'description':
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
        self.LF = 'R1P1'
        self.HF = 'R1P2'
        self.term_chars = '\n'  # visa.LF
        DRIVER.__init__(self)
        self.error = 0
        self.islf = None

    def query(self, cmd):
        if not self.dev:
            return None
        # ans = self.dev.ask(cmd)
        ans = self.dev.query(cmd)
        return ans

    def Init(self, ini, ch=1):
        self.error = DRIVER.Init(self, ini, ch)

        self.out = 'term'
        try:
            self.out = self.conf['init_value']['output']
            self.out = fstrcmp(self.out, ('term', 'rc'), n=1, cutoff=0, ignorecase=True)[0]
        except KeyError:
            pass
        if self.out == 'rc':
            self.LF = 'R1P1R2P1'
            self.HF = 'R1P2R2P2'
        else:
            self.LF = 'R1P1R2P0'
            self.HF = 'R1P2R2P0'

        self.swfreq = 1e9
        try:
            self.swfreq = self.conf['init_value']['swfreq']
        except KeyError:
            pass
        return self.error

    def SetFreq(self, f):
        if f <= self.swfreq:
            cmd = self.LF
        else:
            cmd = self.HF
        ans = self.query(cmd)
        return 0, f

    def Quit(self):
        return 0


if __name__ == '__main__':
    import io
    import numpy as np
    import time

    ini = format_block("""
                    [DESCRIPTION]
                    DESCRIPTION = RC TX Switch
                    TYPE = Custom
                    VENDOR = 
                    SERIALNR = 
                    DEVICEID = 
                    DRIVER = sw_rc_tx
                    CLASS = SWController

                    [INIT_VALUE]
                    FSTART = 0
                    FSTOP = 18e9
                    FSTEP = 0.0
                    GPIB = 2
                    OUTPUT = term
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
