import os
import umdutil
import scipy

umdpath=umdutil.getUMDPath()
dotfile = umdutil.GetFileFromPath('largeMSC-auto-virt.dot', umdpath)

testfreqs = scipy.arange(150e6,1e9,100e6).tolist()

cdict = {"autosave_filename": 'msc-autosave.p',
         "pickle_output_filename": 'msc-autocorrelation-virt.p',
         "pickle_input_filename": None,
         "rawdata_output_filename": 'out_raw_autocorrelation-%s-virt.dat',
         "processeddata_output_filename": 'out_processed_autotocorrelation-%s-virt.dat',
         "log_filename": 'msc.log',
         "logger": ['stdlogger'],
         "minimal_autosave_interval": 3600,
         "descriptions": ['empty'],
         "measure_parameters": [{'dotfile': dotfile,
                                 'delay': 0,
                                 'freqs': testfreqs,
                                 'SGLevel': -20,
                                 'leveling': None,
                                 'toffsets': [1],
                                 'ntunerpos': [360],     
                                 'names': {'sg': 'sg',
                                           'a1': 'a1',
                                           'a2': 'a2',
                                           'ant': 'ant',
                                           'pmfwd': 'pm1',
                                           'pmbwd': 'pm2',
                                           'fp': ['fp1','fp2','fp3','fp4','fp5','fp6','fp7','fp8'], 
                                           'tuner': ['tuner1']
                                           }
                                }],
         "evaluation_parameters": [{"lag": None,
                                    "alpha": 0.05,
                                    "rho": 0.44,
                                    "rho0": None,
                                    "skip": None,
                                    "every": 1,
                                    "offset": 0
                                    }
                                ]
        }
