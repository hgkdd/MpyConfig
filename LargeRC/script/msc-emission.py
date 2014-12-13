import os
import sys
import gzip
import pprint
try:
    import cPickle as pickle
except ImportError:
    import pickle
import MSC
import umddevice
import umdutil


cdict = {"autosave_filename": 'msc-autosave.p',
         "pickle_output_filename": 'msc-emission.p',
         "after_measurement_pickle_file": 'msc-emission-after-measure.p',
         "pickle_input_filename": 'msc-eutcal.p',
         "rawdata_output_filename": 'out_raw_emission-%s.dat',
         "processeddata_output_filename": 'out_processed_emission-%s.dat',
         "log_filename": 'msc.log',
         "logger": ['stdlogger'],
         "minimal_autosave_interval": 3600,
         "descriptions": ['EUT'],
         "measure_parameters": [{'dotfile': 'largeMSC_emission.dot',
                                 'delay': 1,
                                 'freqs': None,
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


def myopen (name, mode):
   if name[-3:] == '.gz':
      return gzip.open(name, mode)
   else:
      return file(name, mode)

def update_conf (cdict):
    try:
        import config
        cdict.update(config.cdict)
        print "Configuration updated from 'config.py'."
    except ImportError:
        pass
    
    if len(sys.argv)>1:
        for name in sys.argv[1:]:
            try:
                _mod = __import__(name[:name.rindex('.')])
                cdict.update(getattr(_mod, 'cdict'))
                print "Configuration updated from '%s'."%name
            except:
                try:
                    dct=eval(name)
                    if type(dct) == type({}):
                        cdict.update(dct)
                        print "Configuration updated from '%s'."%str(dct)
                except:
                    pass

def load_from_autosave(fname):
    msc=None
    cmd=None
    if os.path.isfile(fname):
        try:
            pfile = myopen(fname, "rb")
            msc=pickle.load(pfile)
            cmd=msc.ascmd
            if msc:
                msg = "Auto save file %s found.\ncmd: %s\n\nResume: Resume Measurement\nNew: Start new."%(fname, cmd)
                but = ["Resume", "New"]
                answer = msc.messenger(msg, but)
                #answer=0
                if answer == but.index('Resume'):
                    startnew = False
                else:
                    del msc
                    del cmd
                    msc=None
                    cmd=None
        except IOError, m:
            # this is no problem
            msc.messenger("IOError during check for autosave-file: %s\nContinue with normal operation..."%m, [])
        except (UnpicklingError, AttributeError, EOFError, ImportError, IndexError), m:
            # unpickle was not succesful, but we will continue anyway
            # user can decide later if he want to finish.
            msc.messenger("Error during unpickle of autosave-file: %s\nContinue with normal operation..."%m, []) 
        except:
            # raise all unhadled exceptions
            raise
    return msc,cmd

def make_logger_list(msc, clogger):
    logger = []
    for _l in clogger:
        _lst = _l.split('.')   # _lst can be e.g. [stdlogger] or [custom, Filetablogger]
        _mod=None
        if len(_lst)==1:
            # no module given
            _mod = msc    
        elif len(_lst)==2:
            try:
                _mod = __import__(_lst[0])
            except ImportError, m:
                _mod = None
                msc.messenger("ImportError: %s"%m, [])
        if _mod:
            try:
                logger.append(getattr(msc,_l))
            except AttributeError, m:
                msc.messenger("Logger not found: %s"%m, [])
    if not len(logger):  #empty
        logger=[msc.stdlogger] # fall back to stdlogger
    return logger[:]


if __name__ == '__main__':

    update_conf(cdict)
    print "Configuration values:"
    print
    pprint.pprint (cdict)
            
    msc,cmd=load_from_autosave(cdict['autosave_filename'])
            
    if not msc:
        if cdict['pickle_input_filename']:
            pfile = myopen(cdict['pickle_input_filename'], "rb")
            print "Loading input pickle file '%s'..."%cdict['pickle_input_filename']
            msc=pickle.load(pfile)
            pfile.close()
            print "...done"
        else:
            msc=MSC.MSC()
        msc.setLogFile(cdict['log_filename'])   
        logger = make_logger_list(msc,cdict['logger'])
        msc.setLogger(logger)
        msc.setAutoSave(cdict['autosave_filename'])
        msc.SetAutoSaveInterval(cdict['minimal_autosave_interval'])
    
        descriptions = cdict['descriptions'][:]
        for _i,_des in enumerate(cdict['descriptions']):
            try:
                mp = cdict['measure_parameters'][_i]
            except IndexError:
                mp = cdict['measure_parameters'][0]
            mp['description']=_des
            try:
                ep = cdict['evaluation_parameters'][_i]
            except IndexError:
                ep = cdict['evaluation_parameters'][0]
            ep['description']=_des
            domeas=True
            doeval=True
            if msc.rawData_Emission.has_key(_des):
                domeas=False
                doeval=False
                msg = """"
                Measurement with description '%s' allready found in MSC instance.\n
                How do you want to proceed?\n\n
                Continue: Continue with Measurement.\n
                Skip: Skip Measurement but do Evaluation.\n
                Break: Skip Measurement and Evaluation.\n
                Exit: Exit Application
                """%(_des)
                but = ["Continue", "Skip", "Break", "Exit"]
                answer = msc.messenger(msg, but)
                #answer=0
                if answer == but.index('Break'):
                    continue
                elif answer == but.index('Exit'):
                    sys.exit()
                elif answer == but.index('Continue'):
                    domeas=True
                    doeval=True
                elif answer==but.index('Skip'):
                    domeas=False
                    doeval=True
                else:
                    # be save and do nothing
                    continue
            if domeas:        
                msc.Measure_Emission(**mp)
                pickle.dump(msc, file(cdict["after_measurement_pickle_file"], 'wb'),2)
            if doeval:
                msc.OutputRawData_Emission(fname=cdict["rawdata_output_filename"]%_des)
                msc.Evaluate_Emission(**ep)
        msc.OutputProcessedData_Emission(fname=cdict["processeddata_output_filename"]%("_".join(descriptions)))
    else:
        msg="Select description to use.\n"
        but = []
        for _i,_des in enumerate(cdict['descriptions']):
            msg+='%d: %s'%(_i,_des)
            but.append('%d: %s'%(_i,_des))    
        answer=msc.messenger(msg, but)
        try:
            mp = cdict['measure_parameters'][answer]
        except IndexError:
            mp = cdict['measure_parameters'][0]
        mp['description']=cdict['descriptions'][answer]
        exec(cmd)
        
    if os.path.isfile(cdict['pickle_output_filename']):
        msg = "Pickle file %s allready exist.\n\nOverwrite: Overwrite file\nAppend: Append to file."%(cdict['pickle_output_filename'])
        but = ["Overwrite", "Append"]
        answer = msc.messenger(msg, but)
        if answer == but.index('Overwrite'):
            mode = 'wb'
        else:
            mode = 'ab'
    else:
        mode = 'wb'
    try:
        msc.messenger(umdutil.tstamp()+" pickle results to '%s' ..."%(cdict['pickle_output_filename']), [])
        pf = myopen(cdict['pickle_output_filename'], mode)
        pickle.dump(msc, pf,2)
        msc.messenger(umdutil.tstamp()+" ...done.", [])
    except:
        msc.messenger(umdutil.tstamp()+" failed to pickle to %s"%(cdict['pickle_output_filename']), [])
        raise
    else:
        # remove autosave file after measurement is completed and class instance was pickled
        try:
            os.remove(cdict['autosave_filename'])
        except:
            pass
