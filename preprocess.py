import mne
import numpy as np
import matplotlib.pyplot as plt
import os

if protocol == 'WORDS':
    import config_WORDS as cfg

if protocol == 'PP':
    import config_PP as cfg


## logging info ###
import logging
from datetime import datetime

logname = './logs/' + datetime.now().strftime('log_%Y-%m-%d.log')
logging.basicConfig(filename=logname,level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)


def preprocess_data(protocol, vhdr_fname, sub_name, bad_sub_chan=[],  save=False, verbose=True, plot=True):

    '''
    This function preprocess the data :
        - import data
        - channels correction (define stim chan and chan type, names to match the montage,
                              Cz creation, HEOG/VEOG, re-ref, interpolation,..)
        - apply filter on data (notch 50H and 0.1-40Hz High pass)
        - save preproc data of interest (from 1st trig-3s to last trig+3s)
        in fif format, with '_preproc' extention.

    If 'verbose' set to True, print informations.
    If 'plot' set to True, plot data.
    If 'save' set to True, save the data.
    '''

    #################### Load data ####################
    data = mne.io.read_raw_egi(vhdr_fname, eog=None, misc=None, exclude=None, include=None, preload=True, verbose=None)


    sfreq = data.info['sfreq']
    event_id = data.event_id
    print(event_id)

    # set montage
    coordinatesfile = vhdr_fname + '/coordinates.xml'
    montage = mne.channels.read_dig_egi(coordinatesfile)
    data.set_montage(montage, raise_if_subset=False)

    if verbose:
        print(data.info)
        print('montage : ', montage)
        data.plot_sensors(kind='3d')

    ############# Set data general info ##############
    data.info['proj_name'] = cfg.proj_name
    data.info['subject_info'] = {'his_id' : sub_name}

    ################ Channels operations ##############
    # set stim chan type
    mapping_type = {'STI 014': 'stim'}
    data.set_channel_types(mapping_type)

    # prepare Cz chan
#    Czcopy = data.copy().pick_channels(['E55']).get_data()
#    Czzero = np.zeros((1,np.size(Czcopy)))
#    infoCz = mne.create_info(['Cz'], sfreq, ['eeg'], montage='GSN-HydroCel-129')
#    raw_Cz = mne.io.RawArray(Czzero, infoCz)
#    data.add_channels([raw_Cz], force_update_info=True)

    if verbose:
        print(data.info)
    logger.info('Raw data info ch_names: ,%s', data.info['ch_names'])
    logger.info('Raw data info channels: ,%s', len(data.info['ch_names']))
    logger.info('Raw data info highpass: ,%s', data.info['highpass'])
    logger.info('Raw data info lowpass: ,%s', data.info['lowpass'])
    logger.info('Raw data info sfreq: ,%s', data.info['sfreq'])


    if plot:
        data.plot(show_options=True, block=True) # scaling set to eeg=20e-6, eog=150e-6

    #################### Filters ####################
    # notch filter around 50hz
    if plot:
        picks_psd_plot = mne.pick_types(data.info, eeg=True, selection=['E15','E11', 'E55', 'E62','E75', 'E108', 'E45', 'E122', 'E33'])
        data.plot_psd(area_mode='range', tmax=10.0, picks = picks_psd_plot, average=False)

    picks_eeg = mne.pick_types(data.info, eeg=True)
    data.notch_filter(np.arange(50, 150, 50), picks=picks_eeg, filter_length='auto', phase='zero-double') #i write 150 instead of 200
    # band pass filter around 1-25Hz
    data.filter(cfg.highpass, cfg.highcut, method='fir', phase='zero-double', fir_design='firwin2')

    if plot:
        picks_psd_plot = mne.pick_types(data.info, eeg=True, selection=['E15','E11', 'E55', 'E62','E75', 'E108', 'E45', 'E122', 'E33'])
        data.plot_psd(area_mode='range', tmax=10.0, picks = picks_psd_plot, average=False)

    ########### Create HEOG and VEOG chans ###########
    chan1 = data.copy().pick_channels(['E25']).get_data()
    chan2 = data.copy().pick_channels(['E127']).get_data()
    VEOGL = chan1 - chan2
    infoVEOGL = mne.create_info(['VEOGL'], sfreq, ['eog'])
    raw_VEOGL = mne.io.RawArray(VEOGL, infoVEOGL)

    chan1 = data.copy().pick_channels(['E8']).get_data()
    chan2 = data.copy().pick_channels(['E126']).get_data()
    VEOGR = chan1 - chan2
    infoVEOGR = mne.create_info(['VEOGR'], sfreq, ['eog'])
    raw_VEOGR = mne.io.RawArray(VEOGR, infoVEOGR)

    chan1 = data.copy().pick_channels(['E32']).get_data()
    chan2 = data.copy().pick_channels(['E1']).get_data()
    HEOG = chan1 - chan2
    infoHEOG = mne.create_info(['HEOG'], sfreq, ['eog'])
    raw_HEOG = mne.io.RawArray(HEOG, infoHEOG)

    data.add_channels([raw_VEOGL, raw_VEOGR], force_update_info=True)  #TODO Only VEOG added for now

    #################### Set bad chans ####################
    ## Manual check
    print(data.info)
    print("bad_sub_chan", bad_sub_chan)
    if len(bad_sub_chan)==0:
        print('no bad channels for subject')
    else:
        data.info['bads'] = bad_sub_chan
    print(data.info)

    ## Manual check
    datacheck = data.copy()
    events = mne.find_events(datacheck, stim_channel='STI 014')
    evoked = mne.Epochs(datacheck, events=events, tmin=-0.2, tmax=1.2).average()
    evoked.plot(titles='Global average triggers, any sensorys bad?' +sub_name)
    data.plot(show_options=True, title='Indicate bad sensors manually', block=True)
    print(data.info)

    data.set_channel_types({'E8':'misc','E25':'misc','E17':'misc','E126':'misc','E127':'misc'})

    data.info['bads'].extend(['E129']) # + ['Cz']
    if plot:
        data.plot_sensors(kind='3d', ch_type ='eeg', title='Sensory positions, Red ones & Cz are indicated as bads ')

    logger.info('Bad channels : ,%s', data.info['bads'])


    #################### Interpollation ####################
    print ('Bad channels are interpolated') # used only to calculate average ref (for now)
    data.interpolate_bads(reset_bads=False,origin=(0., 0., 0.04))
    ### Pay ATTENTION! All bad channels are interpolated, this we did to be able to interpolate the Cz channel with only good ones, and is necessary for source reconstruction.
    #PAY ATTENTION : keep using (for pick_types, epochs etc.) " exclude=[] " otherwise the bads get deleted!
    print(data.info['bads'])
    data.info['bads'].remove('E129')
    print(data.info['bads'])
    if plot:
        data.plot(show_options=True, block=True) # scaling set to eeg=20e-6, eog=150e-6
        data.plot_sensors(kind='3d', ch_type ='eeg', title='Sensory positions, Red ones are indicated as bads ')

    #################### Re-Referencing ####################
    data.set_eeg_reference(ref_channels='average', projection=False) # Set EEG average reference

    #################### save preprocessed data of interest ####################
    if save:
        #Export only data of interest : from first trig -3s to last trig + 3s
        events = mne.find_events(data, stim_channel='STI 014')
        event_names = np.zeros((events.shape[0],), dtype='S10') # new array one column of zero's with max lenght of 10 caracters

        for x in range(events.shape[0]): # loop over rows
            value = events[x, 2] # take each 3th column
            new_value = [k for k,v in event_id.items() if v==value][0]
            event_names[x] = new_value
        good_events = events[(event_names!=b'Rest') & (event_names!=b'Code') & (event_names!=b'star') & (event_names!=b'rest'), :] # all events where names is not 'rest'

        if verbose:
            print(data.info)
            print(data.ch_names)
            print("sfreq : ", sfreq)

        i_start = int(good_events[0][0]/data.info['sfreq']-3)
        i_stop =  int(good_events[-1][0]/data.info['sfreq']+3)

        data_name = cfg.data_preproc_path + data.info['subject_info']['his_id'] + cfg.prefix_processed
        print("Saving data : " + data_name)
        if sub_name == 'TWB1_LG':  # or sub_name == 'TWB1_PP':
            data.save(data_name, tmin=cfg.i_start_TWB1, tmax=cfg.i_stop_TWB1, overwrite=True)
        elif sub_name == 'TPC2_LG':
            data.save(data_name, tmin=cfg.i_start_TPC2, tmax=cfg.i_stop_TPC2, overwrite=True)
        else:
            data.save(data_name, tmin=i_start, tmax=i_stop, overwrite=True)
        logger.info("Saved preprocessed data " + data_name)
        ######For EGI subjects, save stimulation name dictionary #######
        nameStimDict = cfg.stimDict_path + data.info['subject_info']['his_id'] + cfg.prefix_stimDict ## For the stimuli dictionary (names of stimuli given automatically vs ones we gave the stimuli)
        np.save(nameStimDict, event_id)
        logger.info("Saved stimdict data " + nameStimDict)


    if plot:
        scalings=dict( eeg=20e-6, eog=100e-6, misc=20e-6)
        data.plot(show_options=True, scalings=dict(eeg=20e-6, eog=100e-6),block=True)
        eventplot = mne.viz.plot_events(events, data.info['sfreq'])
        eventplot = mne.viz.plot_events(good_events, data.info['sfreq'])

    return data
