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
        self.term_chars = '\n'
        DRIVER.__init__(self)
        self._states12 = {'LFAMP':
                              {'LFANT': 'R1P1R2P1',
                               'HFANT': 'R1P1R2P2',
                               'TERM': 'R1P1R2P0'
                               },
                          'HFAMP':
                              {'LFANT': 'R1P2R2P1',
                               'HFANT': 'R1P2R2P2',
                               'TERM': 'R1P2R2P0'
                               },
                          'DIRECT':
                              {'LFANT': 'R1P0R2P1',
                               'HFANT': 'R1P0R2P2',
                               'TERM': 'R1P0R2P0'
                               },
                          'safe': 'R1P0R2P0'
                          }
        # LF:
        #     0dB:
        #            PM:  1010
        #            REC: 1110
        #    20dB:
        #            PM:  1100
        #            REC: 1000
        # HF:
        #     0dB:
        #            PM:  0001
        #            REC: 0101
        #    20dB:
        #            PM:  0111
        #            REC: 0011
        self._states3456 = {'LF': {'0dB': {'PM':    'R3P1R4P0R5P1R6P0',
                                           'REC':   'R3P1R4P1R5P1R6P0',
                                           'safe':  'R3P0R4P0R5P0R6P0'},
                                   '20dB': {'PM':   'R3P1R4P1R5P0R6P0',
                                            'REC':  'R3P1R4P0R5P0R6P0',
                                            'safe': 'R3P0R4P0R5P0R6P0'}
                                   },
                            'HF': {'0dB': {'PM':    'R3P0R4P0R5P0R6P1',
                                           'REC':   'R3P0R4P1R5P0R6P1',
                                           'safe':  'R3P0R4P0R5P0R6P0'},
                                   '20dB': {'PM':   'R3P0R4P1R5P1R6P1',
                                            'REC':  'R3P0R4P0R5P1R6P1',
                                            'safe': 'R3P0R4P0R5P0R6P0'}
                                   },
                            'safe': 'R3P0R4P0R5P0R6P0'
                            }
        # SG direkt in die Termination
        # PM2 und REC an 50 Ohm (REC ueber 20 dB)
        # Alle Antennen: open
        # Fwd und Rev PM: undefiniert
        self._safe = self._states12['safe'] + self._states3456['safe']      # 'R1P0R2P0R3P0R4P0R5P0R6P0'
        # print sw
        # save settings
        self.query(self._safe)
        self.query('R3P1R4P1')   # LFrx, Amp, PM
        self.RxLF = True
        self.RxAtt = True
        self.RxPM = True
        self.error = 0
        #self.islf = None

    def _rx_logic(self):
        lf = self.RxLF
        att = self.RxAtt
        pm = self.RxPM
        if lf:
            if att:
                if pm:
                    cmd = self._states3456['LF']['20dB']['PM']   # 'R3P1R4P1R5P0R6P0'
                else:
                    cmd = self._states3456['LF']['20dB']['REC']   # 'R3P1R4P0R5P0R6P0'
            else:
                if pm:
                    cmd = self._states3456['LF']['0dB']['PM']   # 'R3P1R4P0R5P1R6P0'
                else:
                    cmd = self._states3456['LF']['0dB']['REC']   # 'R3P1R4P1R5P1R6P0'
        else:
            if att:
                if pm:
                    cmd = self._states3456['HF']['20dB']['PM']   # 'R3P0R4P1R5P1R6P1'
                else:
                    cmd = self._states3456['HF']['20dB']['REC']   # 'R3P0R4P0R5P1R6P1'
            else:
                if pm:
                    cmd = self._states3456['HF']['0dB']['PM']   # 'R3P0R4P0R5P0R6P1'
                else:
                    cmd = self._states3456['HF']['0dB']['REC']   # 'R3P0R4P1R5P0R6P1'
        self.query(cmd)


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

#    def _islf(self):
#        ans = self.query('')
#        R3 = self.LF[:4]
#        R6 = self.LF[4:]
#        return (R3 in ans) and (R6 in ans)

    def _rx_lf(self):
        self.RxLF = True
        self._rx_logic()

    def _rx_hf(self):
        self.RxLF = False
        self._rx_logic()

    def _tx_lf(self):
        ans=self.query(self._states12['LFAMP']['LFANT'])
        return ans

    def _tx_hf(self):
        ans=self.query(self._states12['HFAMP']['HFANT'])
        return ans

    def SetFreq(self, f):
        if f <= self.swfreq:
            self._tx_lf()
            self._rx_lf()
        else:
            self._tx_hf()
            self._rx_hf()
        return 0, f

    def SetAtt(self, state=True):
        """
        :param state: True (default) Att on, False: Att off
        :return: answer from query
        """
        self.RxAtt = state
        self._rx_logic()
        return 0

    def Quit(self):
        self.query(self._safe)
        self.query('R3P1R4P1')
        return 0


if __name__ == '__main__':
    import io
    import numpy as np
    import time

    ini = format_block("""
                    [DESCRIPTION]
                    DESCRIPTION = RC RXTX Switch
                    TYPE = Custom
                    VENDOR = 
                    SERIALNR = 
                    DEVICEID = 
                    DRIVER = sw_rc_rxtx
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
    # while True:
    #     cmd = input('Input cmd (q=quit): ')
    #     if cmd == 'c':
    #         break
    #     ans = sw.query(cmd)
    #     print(ans)
    for f in np.linspace(0,4.2e9,10):
        print(f, sw.SetFreq(f))
        print("Att On: ", sw.SetAtt())
        time.sleep(1)
        print("Att Off:", sw.SetAtt(False))
        time.sleep(1)

    sw.Quit()
