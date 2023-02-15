import mne
import numpy as np
import matplotlib.pyplot as plt
import sys
import datetime
import os
import fnmatch
import pandas as pd
import fnmatch
from mne.channels import find_ch_connectivity
from scipy import stats
from mne.stats import spatio_temporal_cluster_1samp_test
from mne.viz import plot_topomap
from mne.time_frequency import tfr_morlet
from mne.stats import permutation_cluster_test
import h5py

## logging info ###
import logging
from datetime import datetime

logname = './logs/' + datetime.now().strftime('log_%Y-%m-%d.log')
logging.basicConfig(filename=logname,level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)


def create_grand_average(protocol, data_evoked_path, conditions, subjects, suffix):
    if protocol == 'WORDS':
        import config_WORDS as cfg
        
    if protocol == 'PP':
        import config_PP as cfg

    AllGrandAverage_ByCond = {}
    for cond in conditions:
        print(cond)
        AllEvokeds =[]
        for sub in subjects:
            print(sub)
            listdir=[]
            for filename in os.listdir(data_evoked_path):
                print(sub)
                print(filename)
                if fnmatch.fnmatch(filename, sub + cfg.prefix_processed.strip('.fif') + '*' + cfg.prefix_ave):
                    print(filename)
                    listdir.append(filename)
            if len(listdir) == 1:
                evoked_name = data_evoked_path + listdir[0]
                print(evoked_name)
                evoked = mne.read_evokeds(evoked_name, condition=cond)#
            else:
                print('ERROR: multiple or no files found, problem in analysis for subject: ' + sub)
                logger.error('multiple or no files found, problem in cleaning for subject: %s' + sub)
                print(listdir)
                exit()
            AllEvokeds.append(evoked)
            print("SHAPE EVOKEDS", np.shape(AllEvokeds)[0])
        print(len(AllEvokeds),cond)
        grand_average = mne.grand_average(AllEvokeds, interpolate_bads=True, drop_bads=False)
        AllGrandAverage_ByCond[cond] = grand_average
    print('AllGrandAverage_ByCond : ', AllGrandAverage_ByCond)
    GA_name = cfg.data_grandaverage_path + suffix + '.npy'
    print(GA_name)
    np.save(GA_name, AllGrandAverage_ByCond)
    return AllGrandAverage_ByCond
    #mne.write_evokeds(GA_name, AllGrandAverage_ByCond)


def fig_grand_average(protocol, conditions, subjects, suffix, plot,save):
    if protocol == 'WORDS':
        import config_WORDS as cfg

    if protocol == 'PP':
        import config_PP as cfg

    GA_name = cfg.data_grandaverage_path  + suffix + '.npy'
    AllGrandAverage_ByCond = np.load(GA_name, allow_pickle=True).item()
    print('AllGrandAverage_ByCond : ', AllGrandAverage_ByCond)

    for cond in conditions:
        print('cond : ', cond)
        title = "Grand Average of " + cond
        times = cfg.topo_times
        GrandAveragefig = AllGrandAverage_ByCond[cond].plot_joint( title=title, show=plot) #, ts_args = dict(ylim=dict(eeg=[-4,4]))
        condTopoFig = AllGrandAverage_ByCond[cond].plot_topomap( times = times, ch_type='eeg', title=title, show=plot)

        if save:
            conds = str(cond.replace('/',''))
            conds.replace("_","")
            png_name = cfg.plot_grandaverage_path + conds + '_' + suffix +'.png'
            png_nametopo = cfg.plot_grandaverage_path + conds + '_' + suffix +'topo.png'
            GrandAveragefig.savefig(png_name)
            condTopoFig.savefig(png_nametopo)
