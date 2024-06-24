import os
import sys
import gzip
import pprint
import pickle

from mpy.env.tem.TEMCell import TEMCell as TEMCell
from mpy.device.device import Device as Device
import mpy.tools.util as util

umdpath=umdutil.getUMDPath()
dotfile = umdutil.GetFileFromPath('largeMSC-immunity.dot', umdpath)

testfreqs = scipy.arange(150e6,1e9,100e6).tolist()

cdict = {"autosave_filename": 'msc-autosave.p',
         "pickle_output_filename": 'msc-immunity.p',
         "pickle_input_filename": 'msc-EUTCal.p',
         "rawdata_output_filename": 'out_raw_immunity-%s.dat',
         "processeddata_output_filename": 'out_processed_immunity-%s.dat',
         "log_filename": 'msc.log',
         "logger": ['stdlogger'],
         "minimal_autosave_interval": 3600,
         "descriptions": ['EUT'],
         "measure_parameters": [{'dotfile': dotfile,
                                 'calibration': 'empty',
                                 'kernel': (None,{}),
                                 'leveling': None,
                                 'freqs': testfreqs,
                                 'names': {'sg': 'sg',
                                           'a1': 'a1',
                                           'a2': 'a2',
                                           'ant': 'ant',
                                           'pmfwd': 'pm1',
                                           'pmbwd': 'pm2',
                                           'fp': [], 
                                           'tuner': ['tuner1'],
                                           'refant': ['refant1'],
                                           'pmref': ['pmref1']
                                           }
                                }]
        }
