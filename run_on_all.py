import preprocess as ppc
import epoch as epo
import cleaning as cln
import evoked as erp
import stats as st
import mne
import sys
import datetime
import os
import fnmatch

from datetime import datetime
import logging

########### Setup for logging ################
protocol = 'WORDS'

if protocol == 'WORDS':
    import config_WORDS as cfg

if protocol == 'PP':
    import config_PP as cfg


# Gets or creates a logger
logname = './logs' + datetime.now().strftime('log_%Y-%m-%d.log')
logging.basicConfig(filename=logname, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)


def run_on_all_subjects():
    '''
    Run the analysis on all the subjects
    '''
    
    cfg.info_subject()

    for sub_number, sub in enumerate(cfg.all_subjects, start=0): # , start=11)

        vhdr_fname = cfg.data_Subject_Dir + sub
        bad_sub_chan = []
        print(cfg.all_subjects[sub_number][0:4])

        if len(cfg.bad_sub_chans[sub_number])==0:
            bad_sub_chan = cfg.bad_sub_chans[sub_number]
        else:
            chanstring = cfg.bad_sub_chans[sub_number]
            chanstring=chanstring.split(",")
            for i in range (len(chanstring)):
                bad_sub_chan.append(chanstring[i])

        sub_name=cfg.id_patient[sub_number]
        print('Process subject %s'%sub_name, "Name file subject : %s"%vhdr_fname,"Protocole : %s"%cfg.protocol[sub_number])
        logger.info('Process subject %s'%vhdr_fname)
        logger.info('Process protocol %s'%cfg.protocol[sub_number])
        print('Bad chans for this subject : ', bad_sub_chan)

        pool = 'controls'

        run_on_specific_subject(vhdr_fname, bad_sub_chan, pool, sub_name)

def run_on_specific_subject(vhdr_fname, bad_sub_chan, pool,sub_name):
    '''
    Run the analysis on a specific subject
    based on run_on_all_autoreject.py code from Lizette
    '''
 
    save = True
    verbose = False
    plot = True #normally True

    data = []
    epochs = []
    epochs_TtP = []

    print("Working on " + sub_name)
    logger.info("Working on " + sub_name)


    ################# Preprocessing Step #############################
    print("Preprocessing data " + sub_name)
    logger.info("Preprocessing data " + sub_name)
    data = ppc.preprocess_data(protocol,vhdr_fname,sub_name, bad_sub_chan, save, verbose, plot)

    ################### Data cleaning ####################
    # ICA
    print("Starting ICA " + vhdr_fname)
    logger.info("Starting ICA " + sub_name)
    fif_fname = cfg.data_preproc_path + sub_name + cfg.prefix_processed
    data = mne.io.read_raw_fif(fif_fname, preload=True)
    data = cln.correct_blink_ICA(data, protocol, save=save, verbose=verbose, plot=plot) # to test, work, adjust threshold,..

    ######################## Epoching step #########################
    print("Epoching data " + sub_name)
    logger.info("Epoching data " + sub_name)

    ##Find files
    listdir=[]
    for filename in os.listdir(cfg.data_preproc_path):
         if fnmatch.fnmatch(filename, sub_name + '*ICA.fif'):
             #print(filename)
             listdir.append(filename)
    print()
    if len(listdir) == 1:

        if protocol == 'WORDS':
            import config_WORDS as cfg
            fif_fname = cfg.data_preproc_path + listdir[0]
            data = mne.io.read_raw_fif(fif_fname, preload=True)
            epochs = epo.get_epochs(data,protocol=protocol, save=save, verbose=verbose, plot=plot)

        if protocol == 'PP':
            import config_PP as cfg
            fif_fname = cfg.data_preproc_path + listdir[0]
            data = mne.io.read_raw_fif(fif_fname, preload=True)
            epochs = epo.get_epochs(data,protocol=protocol, save=save, verbose=verbose, plot=plot)

        if save:
            epochs_name = cfg.data_epochs_path + listdir[0].strip('.fif') + cfg.prefix_epochs_PPAP
            epochs.save(epochs_name, overwrite=True)
            logger.info("Saved Epoched data " + epochs_name)

    else:
        print('ERROR: multiple or no files found, problem in analysis for subject: ' + sub_name)
        logger.error('multiple or no files found, problem in cleaning for subject: %s' + sub_name)
        print(listdir)
        exit()


    ################### Data cleaning ####################
    # Autorejection
    print("Starting cleaning using Autoreject " + vhdr_fname)

    ##Find files
    listdir=[]
    for filename in os.listdir(cfg.data_epochs_path):
         if fnmatch.fnmatch(filename, sub_name + '*-epo.fif'):
             #print(filename)
             listdir.append(filename)
    print()
    if len(listdir) == 1:
         fif_fname = cfg.data_epochs_path + listdir[0]
         epochsICA = mne.read_epochs(fif_fname, proj=False, verbose=True, preload=True)
         epochsICA.average()#.plot()
         print(epochs)
         print(save)
         epochsAr = cln.autorejection_epochs(epochsICA,fif_fname, protocol, save=save, verbose=verbose, plot=plot)
    else:
        print('ERROR: multiple or no files found, problem in analysis for subject: ' + sub_name)
        logger.error('multiple or no files found, problem in cleaning for subject: %s' + sub_name)
        print(listdir)
        exit()


    ######################## Evoked step #########################
    ######################## create evoked dictionary
    print("Starting evoked step " + vhdr_fname)
    logger.info("Starting evoked step %s" + vhdr_fname)

    ##Find files
    listdir=[]
    for filename in os.listdir(cfg.data_epochs_path):
         if fnmatch.fnmatch(filename, sub_name + '*_ar.fif'):
             #print(filename)
             listdir.append(filename)
    print(listdir)
    
    if len(listdir) == 1:
        fif_fname = cfg.data_epochs_path + listdir[0]
        print(fif_fname)
        epochsar = mne.read_epochs(fif_fname, proj=False, verbose=True, preload=True)
        evoked_dict = erp.create_ERP_egi(epochsar, sub_name, fif_fname, protocol, plot=plot, save=save)

    else:
        print('ERROR: multiple or no files found, problem in analysis for subject: ' + sub_name)
        print(listdir)
        logger.error('multiple or no files found, problem in evoked step for subject: %s' + sub_name)
        exit()


    ######################## ERP stats step #########################
    print("Starting statistics " + vhdr_fname)

    ##Find files
    listdir=[]
    for filename in os.listdir(cfg.data_epochs_path):
         if fnmatch.fnmatch(filename, sub_name + '*_ar.fif'):
             #print(filename)
             listdir.append(filename)
    print(listdir)
    if len(listdir) == 1:
        fif_fname = cfg.data_epochs_path + listdir[0]
        print(fif_fname)
        epochsar = mne.read_epochs(fif_fname, proj=False, verbose=True, preload=True)
        epochsar = epochsar.pick_types(eeg=True, eog=False)
        # print(epochsar)
        logger.info("Starting statistics %s" + listdir[0])

        if protocol == 'WORDS':

            cond1 = "TW/C"
            cond2 = "TW/I"
            equalizer = [['TW', 'C'],['TW', 'I']]
            st.perm_SpatTemp_Ttest(sub_name, epochsar, protocol, cond1, cond2, equalizer, save, verbose, plot)

            cond1 = "TW/C"
            cond2 = "TPW"
            equalizer = [['TW', 'C'],['TPW']]
            st.perm_SpatTemp_Ttest(sub_name, epochsar, protocol, cond1, cond2, equalizer, save, verbose, plot)

            cond1 = "TW/I"
            cond2 = "TPW"
            equalizer = [['TW', 'I'],['TPW']]
            st.perm_SpatTemp_Ttest(sub_name, epochsar, protocol, cond1, cond2, equalizer, save, verbose, plot)

            #cond1 = "TW"
            #cond2 = "TPW"
            #equalizer = [['TW'],['TPW']]
            #st.perm_SpatTemp_Ttest(sub_name, epochsar, protocol, cond1, cond2, equalizer, save, verbose, plot)


        if protocol == 'PP':

            cond1 = "PP"
            cond2 = "AP"
            equalizer = [['PP'],['AP']]
            st.perm_SpatTemp_Ttest(sub_name, epochsar, protocol, cond1, cond2, equalizer, save, verbose, plot)
            

    else:
        print('ERROR: multiple or no files found, problem in analysis for subject: ' + sub_name)
        print(listdir)
        logger.error('multiple or no files found, problem in evoked step for subject: %s' + sub_name)
        exit()


################################## What to run #################################

if __name__ == '__main__' :

    print('ici0')

    #Log stuffs
    '''
    old_stdout = sys.stdout
    now = datetime.datetime.now()
    log_name = now.strftime("%Y-%m-%d %H:%M") + ".log"
    log_rep = './logs/'
    log_file = open(log_rep+log_name,"w")
    sys.stdout = log_file
    '''

    print('MNE VERSION : ', mne.__version__)

    ######  Exemple 1 : run on all . Suppose that bad_sub_chans is set.
    run_on_all_subjects()

    ######  CONTROLS : run on all, specific analysis per subject . Suppose that bad_sub_chans is set.
    #########Run preprocessing & first ERP on all subjects the same:

    #highpass = 0.1
    #reject = {'eeg': 150e-6, 'eog': 150e-6} ## setting without ica
    #preprocessing(data_erp_path, highpass, reject, data_preproc_path, montageFile, plot_events_path)


    '''
    sys.stdout = old_stdout
    log_file.close()
    '''
