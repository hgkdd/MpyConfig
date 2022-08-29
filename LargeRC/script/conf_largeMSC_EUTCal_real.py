import os
import umdutil
import scipy

umdpath=umdutil.getUMDPath()
dotfile = umdutil.GetFileFromPath('largeMSC_EUTcalib.dot', umdpath)

testfreqs = scipy.arange(1e9,4.3e9,100e6).tolist()

cdict = {"autosave_filename": 'msc-autosave.p',
         "pickle_output_filename": 'msc-eutcal.p',
         "pickle_input_filename": 'I:\\Messungen\\largeMSC\\Cal_2004\\Nicht_widerlegte_Fakten\\MainCal-LargeMSC-10-2004-converted.p',
         "after_measurement_pickle_file": 'msc-eutcal-after-measure.p',
         "rawdata_output_filename": 'out_raw_eutcal-%s.dat',
         "processeddata_output_filename": 'out_processed_eutcal-%s.dat',
         "log_filename": 'msc.log',
         "logger": ['stdlogger'],
         "minimal_autosave_interval": 3600,
         "descriptions": ['RegTP'],
         "measure_parameters": [{'dotfile': dotfile,
                                 'delay': 1,
                                 'freqs': testfreqs,
                                 'SGLevel': -10,
                                 'leveling': None,
                                 'calibration': 'empty',
                                 'names': {'sg': 'sg',
                                           'a1': 'a1',
                                           'a2': 'a2',
                                           'ant': 'ant',
                                           'pmfwd': 'pm1',
                                           'pmbwd': 'pm2',
                                           'tuner': ['tuner1'],
                                           'refant': ['refant'],
                                           'pmref': ['pmref1']
                                           }
                                }]
        }
