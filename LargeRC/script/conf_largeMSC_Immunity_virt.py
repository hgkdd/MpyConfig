import os
import umdutil
import scipy

umdpath=umdutil.getUMDPath()
dotfile = umdutil.GetFileFromPath('largeMSC-immunity-virt.dot', umdpath)

testfreqs = scipy.arange(150e6,1e9,100e6).tolist()

cdict = {"autosave_filename": 'msc-autosave.p',
         "pickle_output_filename": 'msc-immunity-virt.p',
         "pickle_input_filename": 'msc-EUTCal.p',
         "rawdata_output_filename": 'out_raw_immunity-%s-virt.dat',
         "processeddata_output_filename": 'out_processed_immunity-%s-virt.dat',
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
