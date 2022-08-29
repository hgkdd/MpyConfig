import os
import umdutil
import scipy

umdpath=umdutil.getUMDPath()
dotfile = umdutil.GetFileFromPath('largeMSC-EUTcalib-virt.dot', umdpath)

testfreqs = scipy.arange(150e6,1e9,100e6).tolist()

cdict = {"autosave_filename": 'msc-autosave.p',
         "pickle_output_filename": 'msc-eutcal-virt.p',
         "pickle_input_filename": 'msc-maincal.p',
         "rawdata_output_filename": 'out_raw_eutcal-%s-virt.dat',
         "processeddata_output_filename": 'out_processed_eutcal-%s-virt.dat',
         "log_filename": 'msc.log',
         "logger": ['stdlogger'],
         "minimal_autosave_interval": 3600,
         "descriptions": ['EUT'],
         "measure_parameters": [{'dotfile': dotfile,
                                 'delay': 0,
                                 'freqs': testfreqs,
                                 'SGLevel': -20,
                                 'leveling': None,
                                 'calibration': 'empty',
                                 'names': {'sg': 'sg',
                                           'a1': 'a1',
                                           'a2': 'a2',
                                           'ant': 'ant',
                                           'pmfwd': 'pm1',
                                           'pmbwd': 'pm2',
                                           'tuner': ['tuner1'],
                                           'refant': ['refant1'],
                                           'pmref': ['pmref1']
                                           }
                                }]
        }
