import mne
import numpy as np
import matplotlib.pyplot as plt
import os


from mne.preprocessing import ICA
from autoreject import get_rejection_threshold
from autoreject import (AutoReject, set_matplotlib_defaults)

## logging info ###
import logging
from datetime import datetime

logname = './logs/' + datetime.now().strftime('log_%Y-%m-%d.log')
logging.basicConfig(filename=logname,level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

if protocol == 'WORDS':
    import config_WORDS as cfg

if protocol == 'PP':
    import config_PP as cfg


def correct_blink_ICA(data, protocol, save=False, verbose=True, plot=True):
    '''
    This function tries to removes blink artefacts from preprocessed data.
    Indeed, data needs to be clean and cuted to relevant to improve the removal.
    the method used is based on ICA projection where we remove the blink composante.
    All the difficulty is to get the purest blink composant !
    This is a first working version - feel free to improve it !
    '''

    picks_eog = mne.pick_types(data.info, eog=True)
    datacopy = data.copy()
    datacopy.filter(1, 10, n_jobs=1, l_trans_bandwidth='auto', h_trans_bandwidth='auto',
    			 picks=picks_eog, filter_length='auto', phase='zero-double')

    eog_id = 0
    eog_events = mne.preprocessing.find_eog_events(datacopy, eog_id, verbose = 'DEBUG')
    average_eog = mne.preprocessing.create_eog_epochs(datacopy).average()
    n_blinks = len(eog_events)

    if verbose:
        print('Nb blink found : ', n_blinks)


    if plot:
        data.plot(events=eog_events)
        average_eog.plot_joint()

    logger.info('Nb blink found : ,%s', n_blinks)

    ################ ICA correction ##################
    if n_blinks >cfg.minBlinksICA:
        logger.info('Too many blinks ICA performed')
        ica = ICA(n_components=cfg.n_components,method=cfg.method, random_state=cfg.random_state)#, fit_params=dict(extended=True)
        #ica = ICA(n_components=None,method=cfg.method, random_state=cfg.random_state)#, fit_params=dict(extended=True)
        #print(ica)

        picks = mne.pick_types(datacopy.info, meg=False, eeg=True, eog=False, stim=False, exclude='bads')

        ###Autorejection (global)###
        #ICA solutions can be affected by high amplitude artifacts, therefore we recommend to determine
        # a reasonable rejection threshold on which data segments to ignore in the ICA. autoreject (global)
        # can be used exactly for this purpose
        #In case you want to fit your ICA on the raw data, you will need an intermediate step, because autoreject only works on epoched data.
        # ICA is ignoring the time domain of the data, so we can simply turn the raw data into equally spaced “fixed length” epochs using ::func::mne.make_fixed_length_events:
        #tstep = 1.0
        ##autorejectEvents = mne.make_fixed_length_events(datacopy, duration=tstep)
        #autorejectEpochs = mne.Epochs(datacopy, autorejectEvents, tmin=0.0, tmax=tstep,baseline=(0, 0))
        #AutorejectGlobal = get_rejection_threshold(autorejectEpochs)
        #print(' AutorejectGlobal : ' , AutorejectGlobal)

        ica.fit(datacopy, picks=picks)#, reject=AutorejectGlobal, tstep=tstep) #decim=cfg.decim,
        if verbose:
            print(ica)
        if plot:
            ica.plot_components()
        logger.info('ICA info = ,%s', ica)

        #eog_epochs =  mne.preprocessing.create_eog_epochs(datacopy, reject=AutorejectGlobal)
        eog_inds, scores = ica.find_bads_eog(datacopy, ch_name=None, threshold=3)

        if verbose:
            print("eog_inds : ", eog_inds)
            print("scores : ", scores)
        logger.info("eog_inds : ,%s", eog_inds)
        if plot:
            #ica.plot_components()
            ica.plot_scores(scores, exclude=eog_inds)
            ica.plot_sources(average_eog)#, exclude=eog_inds)
            title = 'Sources related to %s artifacts (red)'
            ica.plot_properties(datacopy, picks=eog_inds, psd_args={'fmax': 35.},
                            image_args={'sigma': 1.})


        ica.exclude.extend(eog_inds)
        if plot:
            data.plot(events=eog_events)
            ica.plot_sources(datacopy, title=title % 'eog', block=True)
            ica.plot_overlay(average_eog, exclude=eog_inds, show=False)
        ica.apply(data, exclude=eog_inds)
        if plot:
            data.plot(events=eog_events, block=True)
        if save:
            data_name = cfg.data_preproc_path + data.info['subject_info']['his_id'] + cfg.prefix_processed.strip('.fif') + cfg.prefix_ICA
            data.save(data_name, overwrite=True)
            logger.info('saved ICA data', data_name)
            return data
        logger.info('components excluded = %s', eog_inds)
    if save:
        data_name = cfg.data_preproc_path + data.info['subject_info']['his_id'] + cfg.prefix_processed.strip('.fif') + cfg.prefix_noICA
        data.save(data_name, overwrite=True)
        logger.info('saved ICA data', data_name)

    return data




def autorejection_epochs(epochs,fif_fname, protocol, save=False, verbose=True, plot=True):

    n_interpolates = np.array([1, 4, 32])
    consensus_percs = np.linspace(0, 1.0, 11)
    picks = mne.pick_types(epochs.info, meg=False, eeg=True, stim=False,eog=False, exclude=[])

    ar = AutoReject(n_interpolate=n_interpolates, consensus=consensus_percs, picks=picks,
                thresh_method='random_search', random_state=42)
    epochs_clean, reject_log = ar.fit_transform(epochs, return_log=True)

    if plot:
        reject_log.plot_epochs(epochs)
        ar.get_reject_log(epochs).plot()
        epochs_clean.plot(title='Epochs after cleaning')
        epochs_clean.plot_drop_log()

    old = epochs.average()
    png_name = cfg.cleaning_path +  fif_fname.split('/')[-1].strip('.fif') + 'old.png'

    old.plot(spatial_colors=True, show=False, titles='Old data').savefig(png_name)

    new = epochs_clean.average()
    png_name = cfg.cleaning_path +  fif_fname.split('/')[-1].strip('.fif') + 'new.png'
    new.plot(spatial_colors=True, show=False, titles='Cleaned data').savefig(png_name)
    png_name = cfg.cleaning_path +  fif_fname.split('/')[-1].strip('.fif') + 'difference.png'
    difference = mne.combine_evoked([old, - new], weights='equal').plot_joint(show=False, title='Difference raw & cleaned').savefig(png_name)

    if plot:
        plt.show()

    print('Nb epochs uncleaned, %s',len(epochs))
    print('Nb epochs cleaned, %s',len(epochs_clean))
    print('Nb epochs deleted, %s',(len(epochs)-len(epochs_clean)))


    #logger.info('The instances of _AutoReject for each channel type. %s', ar.local_reject)
    #logger.info('Percentage dropped epochs, %s', epochs_clean.drop_log_stats)
    logger.info('Nb epochs uncleaned, %s',len(epochs))
    logger.info('Nb epochs cleaned, %s',len(epochs_clean))
    logger.info('Nb epochs deleted, %s',(len(epochs)-len(epochs_clean)))

    if save:
        data_name = fif_fname.strip('.fif') + cfg.prefix_autoreject
        print(data_name)
        epochs_clean.save(data_name, overwrite=True)
        logger.info('saved cleaned data', data_name)

    return epochs


def ICA_0Artifact (epochs, n_components, all_conditions):
    
    epochs["PP"].average().plot(spatial_colors=True)
    epochsfilt = epochs.copy()
    #epochsfilt.plot_psd(fmin=0.5,fmax=40,tmin=-0.03, tmax=0.03)
    #epochsfilt.plot_psd(tmin=-0.03, tmax=0.03)

    print (epochsfilt)

    epochsfilt.filter(5., 30., n_jobs=2, fir_design='firwin')
   
    ################ ICA correction ##################
    method = 'fastica'  # for comparison with EEGLAB try "extended-infomax" here
    decim = 3  # we need sufficient statistics, not all time points -> saves time
    random_state = 23


    ica = ICA(n_components=n_components, method=method, random_state=random_state)
    picks = mne.pick_types(epochsfilt.info, meg=False, eeg=True, eog=False, stim=False, exclude='bads')
    reject = {'eeg': 100e-6}
    ica.fit(epochsfilt, picks=picks, decim=3, reject=reject)
    print(ica)
    ica.plot_components()

    oaverage_filt = epochsfilt.average()
    oaverage_filt.plot(titles = 'Average ERP (all conditions)')

    ica.plot_sources(oaverage_filt)
    ica.plot_sources(epochsfilt, show=True, block=True)
    ica.plot_properties(epochsfilt, picks=(ica.exclude), psd_args={'fmax': 35.})
    ica.plot_overlay(oaverage_filt, exclude=(ica.exclude), show=False)


    ica.apply(epochs, exclude=(ica.exclude))
    oaverage = epochs.average()
    oaverage.plot(titles = 'Average ERP (all conditions) after 0-artifact ICA')
    epochs["PP"].average().plot(spatial_colors=True)

    return epochs
