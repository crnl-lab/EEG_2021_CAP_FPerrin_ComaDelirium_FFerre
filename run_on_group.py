import mne
import evoked as erp
import stats as st
import numpy as np
import GrandAverage as ga
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
## logging info ###
import logging
from datetime import datetime

########### Setup for logging ################
protocol = 'PP'

# Gets or creates a logger
logname = './logs' + datetime.now().strftime('log_%Y-%m-%d.log')
logging.basicConfig(filename=logname, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)


### start the analysis
def run_on_group():
    '''
    Create a average of all subjects & perform stats etc.
    '''
    print('group1')

    save = True
    verbose = True
    plot = True #normally True



    ################# Preprocessing Step #############################
    if protocol == 'WORDS':
        import config_WORDS as cfg

    if protocol == 'PP':
        import config_PP as cfg

    cfg.info_subject()
    subjects = cfg.id_patient
    print("Averageing subjects " + str(subjects))
    logger.info("Averageing subjects " + str(subjects))

    ## Get GRand Average **
    data_evoked_path = cfg.data_evoked_path
    conditions = cfg.all_conditions
    suffix = cfg.prefix_grandaverage
    data = ga.create_grand_average(protocol, data_evoked_path, conditions, subjects, suffix)

    ##Get figures
    ga.fig_grand_average(protocol, conditions, subjects, suffix, plot, save)


    ##STATS
    if protocol == 'WORDS':
        import config_WORDS as cfg

        cond1 = "TWC"
        cond2 = "TWI"
        evoked_names = cfg.data_grandaverage_path + suffix + '.npy'
        st.perm_SpatTemp_Ttest_GrandAverage(protocol,evoked_names, data_evoked_path, cfg.text_stats_path, cfg.plot_stats_path, subjects, cond1, cond2, cfg.csv_stats_textfile, suffix)

        cond1 = "TWC"
        cond2 = "TPW"
        evoked_names = cfg.data_grandaverage_path + suffix + '.npy'
        st.perm_SpatTemp_Ttest_GrandAverage(protocol,evoked_names, data_evoked_path, cfg.text_stats_path, cfg.plot_stats_path, subjects, cond1, cond2, cfg.csv_stats_textfile, suffix)

        cond1 = "TWI"
        cond2 = "TPW"
        evoked_names = cfg.data_grandaverage_path + suffix + '.npy'
        st.perm_SpatTemp_Ttest_GrandAverage(protocol,evoked_names, data_evoked_path, cfg.text_stats_path, cfg.plot_stats_path, subjects, cond1, cond2, cfg.csv_stats_textfile, suffix)

    if protocol == 'PP':
        import config_PP as cfg
        cond1 = "PP"
        cond2 = "AP"
        evoked_names = cfg.data_grandaverage_path + suffix + '.npy'
        st.perm_SpatTemp_Ttest_GrandAverage(protocol,evoked_names, data_evoked_path, cfg.text_stats_path, cfg.plot_stats_path, subjects, cond1, cond2, cfg.csv_stats_textfile, suffix)


################################## What to run #################################

if __name__ == '__main__' :

    print('group0')

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
    ##group = ['VOLUNTEERS', 'PATIENTS']
    run_on_group()
