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
        self.LF = 'R3P1R6P0'
        self.HF = 'R3P0R6P1'
        self.term_chars = '\n'
        DRIVER.__init__(self)
        self.error = 0
        self.islf = None

    def query(self, cmd):
        if not self.dev:
            return None
        ans = self.dev.query(cmd)
        return ans

    def Init(self, ini, ch=1):
        self.error = DRIVER.Init(self, ini, ch)

        self.out = 'powermeter'
        try:
            self.out = self.conf['init_value']['output']
            self.out = fstrcmp(self.out, ('receiver', 'powermeter'), n=1, cutoff=0, ignorecase=True)[0]
            # print("##############################")
            # print("PM_RX_Out: ", self.out)
            # print("##############################")
            # input("Continue?")
        except KeyError:
            pass

        self.swfreq = 1e9
        try:
            self.swfreq = self.conf['init_value']['swfreq']
        except KeyError:
            pass
        return self.error

    def _islf(self):
        ans = self.query('')
        R3 = self.LF[:4]
        R6 = self.LF[4:]
        return (R3 in ans) and (R6 in ans)

    def SetFreq(self, f):
        if f <= self.swfreq:
            cmd = self.LF
        else:
            cmd = self.HF
        ans = self.query(cmd)
        return 0, f

    def SetAtt(self, state=True):
        """
        :param state: True (default) Att on, False: Att off
        :return: answer from query
        """
        pm = (self.out == 'powermeter')
        if self._islf():
            # logic for LF
            if state:
                # Att is ON
                if pm:
                    cmd = 'R4P1R5P0'
                else:
                    cmd = 'R4P0R5P0'
            else:
                # Att is Off
                if pm:
                    cmd = 'R4P0R5P1'
                else:
                    cmd = 'R4P1R5P1'
        else:
            # logic for HF
            if state:
                # Att is on
                if pm:
                    cmd = 'R4P1R5P1'
                else:
                    cmd = 'R4P0R5P1'
            else:
                # Att is Off
                if pm:
                    cmd = 'R4P0R5P0'
                else:
                    cmd = 'R4P1R5P0'
        # print state, pm, cmd
        ans = self.query(cmd)
        return ans

    def Quit(self):
        return 0


if __name__ == '__main__':
    import io
    import numpy as np
    import time

    ini = format_block("""
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
    ini = io.StringIO(ini)

    sw = SWController()
    sw.Init(ini)
    while True:
        cmd = input('Input cmd (q=quit): ')
        if cmd == 'c':
            break
        ans = sw.query(cmd)
        print(ans)
    # for f in np.linspace(0,4.2e9,10):
    #     print(f, sw.SetFreq(f))
    #     print("Att On: ", sw.SetAtt())
    #     time.sleep(1)
    #     print("Att Off:", sw.SetAtt(False))
    #     time.sleep(1)

    sw.Quit()
