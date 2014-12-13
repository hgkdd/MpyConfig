import os
import umdutil
import scipy

umdpath=umdutil.getUMDPath()
dotfile = umdutil.GetFileFromPath('largeMSC-emission-virt.dot', umdpath)

testfreqs = scipy.arange(150e6,1e9,100e6).tolist()

cdict = {"autosave_filename": 'msc-autosave.p',
         "pickle_output_filename": 'msc-emission-virt.p',
         "pickle_input_filename": 'msc-eutcal.p',
         "rawdata_output_filename": 'out_raw_emission-%s-virt.dat',
         "processeddata_output_filename": 'out_processed_emission-%s-virt.dat',
         "log_filename": 'msc.log',
         "logger": ['stdlogger'],
         "minimal_autosave_interval": 3600,
         "descriptions": ['EUT'],
         "measure_parameters": [{'dotfile': dotfile,
                                 'delay': 0,
                                 'freqs': testfreqs,
                                 'calibration': 'empty',
                                 'receiverconf': None,
                                 'names': {'tuner': ['tuner1'],
                                           'refant': ['refant1'],
                                            'receiver': ['pmref1']
                                           }
                                    }
                                ],
         "evaluation_parameters": [{"empty_cal": 'empty',
                                    "loaded_cal": 'loaded',
                                    "EUT_cal": 'loaded',
                                    "distance": 3.0,
                                    "directivity": 1.5
                                    }]
        }
