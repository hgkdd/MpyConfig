import os
import umdutil
import scipy

umdpath=umdutil.getUMDPath()
dotfile = umdutil.GetFileFromPath('largeMSC_emission-regtp.dot', umdpath)

testfreqs = scipy.arange(1e9,4.3e9,100e6).tolist()

cdict = {"autosave_filename": 'msc-autosave.p',
         "pickle_output_filename": 'msc-emission-eval.p',
         "after_measurement_pickle_file": 'msc-emission-after-measure.p',
         "pickle_input_filename": 'msc-emission.p', #  '..\\eutcal\\msc-eutcal.p',
         "rawdata_output_filename": 'out_raw_emission-%s.dat',
         "processeddata_output_filename": 'out_processed_emission-%s.dat',
         "log_filename": 'msc.log',
         "logger": ['stdlogger'],
         "minimal_autosave_interval": 3600,
         "descriptions": ['RegTP'],
         "measure_parameters": [{'dotfile': dotfile,
                                 'delay': 1,
                                 'freqs': testfreqs,
                                 'calibration': 'empty',
                                 'receiverconf': None,
                                 'names': {'tuner': ['tuner1'],
                                           'refant': ['refant'],
                                            'receiver': ['pmref1']
                                           }
                                    }
                                ],
         "evaluation_parameters": [{"empty_cal": 'empty',
                                    "loaded_cal": 'loaded',
                                    "EUT_cal": 'RegTP',
                                    "distance": 3.0,
                                    "directivity": 1.7
                                    }]
        }
