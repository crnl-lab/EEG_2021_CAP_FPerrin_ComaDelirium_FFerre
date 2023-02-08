import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


## logging info ###
import logging
from datetime import datetime

logname = './logs/' + datetime.now().strftime('log_%Y-%m-%d.log')
logging.basicConfig(filename=logname,level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)


def get_epochs(data, protocol, save=True, verbose=True, plot=True):

    if protocol == 'WORDS':
        import config_WORDS as cfg

    if protocol == 'PP':
        import config_PP as cfg

    SubName = data.info['subject_info']['his_id']

    ########### Renaming of EGI-loaded triggers  ###########
    StimNpy = cfg.stimDict_path + SubName + cfg.prefix_stimDict
    print(StimNpy)
    translate_dict = np.load(StimNpy, allow_pickle=True).item()

    events = mne.find_events(data, stim_channel='STI 014')
    print('Events BEFORE first changes : ', events)
    print('translate_dict : ', translate_dict)
    #eventplot = mne.viz.plot_events(events, data.info['sfreq'])

    new_dict = {}
    new_events = events.copy()
    for key, value in translate_dict.items():
        if key != 'Rest' and key != 'Code' and key != 'rest' and key != 'star' and key != 'IEND':
            new_key = ''.join(x for x in key if x.isdigit())
            #new_key = int(new_key) # retire or ...
        else:
            new_key = key
        new_dict[new_key] = value
    print('new_dict : ', new_dict)

    for (x,y), value in np.ndenumerate(events):
        if y==2:
            new_value = [k for k,v in new_dict.items() if v==value][0] #corect here because one key is associated to one value. better to use inverse dict ?
            if new_value != 'IEND' and new_value  != 'rest' and new_value != 'Code' and new_value != 'Rest' and new_value != 'star':
                new_events[x,y] = new_value

    if verbose:
        print('Events AFTER changes : ', new_events)
    if plot:
        eventplot = mne.viz.plot_events(new_events, data.info['sfreq'])


    ########### Segmetation and rejection ###########
    tmin, tmax = cfg.erp_window_tmin, cfg.erp_window_tmax
    baseline = cfg.erp_baseline
    detrend = cfg.erp_detrend # Either 0 or 1, the order of the detrending. 0 is a constant (DC) detrend, 1 is a linear detrend.

    picks_eeg_eog = mne.pick_types(data.info, eeg=True, eog=True, exclude=[]) #eeg and eog chan for rejection
    #picks_eeg_eog = mne.pick_types(data.info, eeg=True, eog=True, selection =['Cz', 'E55', 'E62', 'E106', 'E7', 'E80', 'E31', 'E79', 'E54', 'E61', 'E78']) #FOR PATIENT TpTP
    epochs = mne.Epochs(data, events=new_events, event_id=cfg.events_id, tmin=tmin, tmax=tmax,
                        baseline=baseline, detrend=detrend, picks=picks_eeg_eog, on_missing='warning',
                        reject=cfg.epochs_reject, preload=True)
    if verbose:
        print('epochs : ', epochs.info)
        print('Number of events :', new_events.size/3)
        #print('Number of redefined events :', events_redef_equal.size)
        print('Number of epochs :', len(epochs))


    if plot:
        epochs.plot_drop_log(subject=SubName)
        epochs.plot(title=SubName, show=True, block=True, scalings=dict(eeg=50e-6, eog=100e-6))  # Here it's possible to click on event to reject
        #epochs["TW/Congurent"].average().plot()
        #epochs["TW/Incongruent"].average().plot()
        #epochs["TPW"].average().plot()


    logger.info('Number of events : ,%s', events.size)
    logger.info('Number of events : ,%s', events.size)
    #gger.info('Number of redefined events :,%s', events_redef_equal.size)
    logger.info('Number of epochs :,%s', len(epochs))
    return epochs

