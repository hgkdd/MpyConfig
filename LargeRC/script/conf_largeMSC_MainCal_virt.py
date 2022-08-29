import os
import umdutil

umdpath=umdutil.getUMDPath()
dotfile = umdutil.GetFileFromPath('largeMSC-maincal-virt.dot', umdpath)

#print dotfile

cdict = {"autosave_filename": 'msc-autosave.p',
         "pickle_output_filename": 'msc-maincal-virt.p',
         "pickle_input_filename": None,
         "rawdata_output_filename": 'out_raw_maincal-%s-virt.dat',
         "processeddata_output_filename": 'out_processed_maincal-virt.dat',
         "log_filename": 'msc.log',
         "logger": ['stdlogger'],
         "minimal_autosave_interval": 3600,
         "descriptions": ['empty', 'loaded'],
         "measure_parameters": [{'dotfile': dotfile,
                                 'delay': 0,
                                 'FStart': 150e6,
                                 'FStop': 4.2e9,
                                 'SGLevel': -20,
                                 'leveling': None,
                                 'ftab': [3,6,10,100,1000],
                                 'nftab': [20,15,10,20,20],
                                 'ntuntab': [[5,2,2,2,2]],
                                 'tofftab': [[7,14,28,28,28]],
                                 'nprbpostab': [8,8,8,8,8],
                                 'nrefantpostab': [1,1,1,1,1],
                                 'names': {'sg': 'sg',
                                           'a1': 'a1',
                                           'a2': 'a2',
                                           'ant': 'ant',
                                           'pmfwd': 'pm1',
                                           'pmbwd': 'pm2',
                                           'fp': ['fp1','fp2','fp3','fp4','fp5','fp6','fp7','fp8'], 
                                           'tuner': ['tuner1'],
                                           'refant': ['refant1'],
                                           'pmref': ['pmref1']
                                           }
                                }]
        }
