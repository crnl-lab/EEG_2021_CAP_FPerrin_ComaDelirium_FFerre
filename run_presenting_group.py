import preprocess as ppc
import epoch as epo
import cleaning as cln
import evoked as erp
import stats as st
import plotting as pl
import mne
import sys
import datetime
import os
import fnmatch
import numpy as np

########### Setup for logging ################
protocol = 'WORDS'

if protocol == 'WORDS':
    import config_WORDS as cfg

if protocol == 'MATHS':
    import config_MATHS as cfg

if protocol == 'PP':
    import config_PP as cfg

if protocol == 'LG':
    import config_LG as cfg


##def run_on_subjects(all_subjects): ##ATTENTION
def run_on_group(all_subjects):


    '''
    Run the analysis on a specific subject
    based on run_on_all_autoreject.py code from Lizette
    '''

    ## CHOOSE CONDITIONS, COLORS, LINESTYLES
    #colors = {'1': "skyblue", '2': "slategray", '3': "black"}
    #linewidth = {'1': 4, '2' : 4, '3' : 4}
    #colors = {"TRUE": "skyblue", "FALSE": "slategray"}
    #colors = {"PP": "skyblue", "AP": "slategray"}
    #colors = {"LS": "skyblue", "LD": "slategray", "GS": "yellowgreen", "GD": "black"}

    picks = "data" # channel name, or data = GFP
    save = True
    verbose = True
    plot = True #normally True
    plot_compare_erp_path = cfg.plot_evoked_group_path ## TO ADD OR CHANGE, make clear folders
    data_evoked_path = cfg.data_grandaverage_path

    sub = 'Grand_Average'
    AllGrandAverage = np.load(all_subjects, allow_pickle=True).item()

    #Creating the conditions

    TWC = AllGrandAverage['TWC']
    TWI = AllGrandAverage['TWI']
    TPW = AllGrandAverage['TPW']

    conditions_compared = [TWC, TWI, TPW]
    plot_cond_name = 'TWC_TWI_TPW'

    '''
    TRUE = AllGrandAverage['TRUE']
    FALSE = AllGrandAverage['FALSE']

    conditions_compared = [TRUE, FALSE]
    plot_cond_name = 'TRUE_FALSE'


    PP = AllGrandAverage['PP']
    AP = AllGrandAverage['AP']

    conditions_compared = [PP, AP]
    plot_cond_name = 'PP_AP'


    LS = AllGrandAverage['LS']
    LD = AllGrandAverage['LD']
    GS = AllGrandAverage['GS']
    GD = AllGrandAverage['GD']
    LSGS = AllGrandAverage['LSGS']
    LSGD = AllGrandAverage['LSGD']
    LDGS = AllGrandAverage['LDGS']
    LDGD = AllGrandAverage['LDGD']


    conditions_compared = [LSGS, LSGD, LDGS, LDGD]
    plot_cond_name = 'LSGS_LSGD_LDGS_LDGD'

    #conditions_compared = [LS, LD]
    #plot_cond_name = 'LS_LD'

    #conditions_compared = [GS, GD]
    #plot_cond_name = 'GS_GD'

    #conditions_compared = [LSGS, LDGS]
    #plot_cond_name = 'LSGS_LDGS'

    #conditions_compared = [LSGD, LDGD]
    #plot_cond_name = 'LSGD_LDGD'

    #conditions_compared = [LSGS, LSGD]
    #plot_cond_name = 'LSGS_LSGD'

    #conditions_compared = [LDGS, LDGD]
    #plot_cond_name = 'LDGS_LDGD'
    '''
    ### ALL THE FIGURES YOU WANT TO SHOW PER SUBJECT ###

    ##show all electrodes:
    pl.create_compare_evoked_group_plot_topo(sub, AllGrandAverage, conditions_compared, plot_cond_name, plot_compare_erp_path, save)

    #pl.create_compare_ERP_plot_topo(sub, AllGrandAverage,conditions_compared, plot_compare_erp_path, save)

    ##Show comparison of electrodes on GFP or an electrode (using picks)
    pl.create_compare_evoked_group_plot(sub, AllGrandAverage, conditions_compared, plot_cond_name, plot_compare_erp_path, picks, save, plot)


    ##Show the average of electrodes in 11 areas
    pl.create_11_evoked_group_plot(sub, AllGrandAverage, conditions_compared, plot_cond_name, plot_compare_erp_path, save, plot)
            # TODO: FABRICE: CHECK IF ALL ELECTRODES ARE IN THE 11 PLOT script => checked by FABRICE 09292020


    ##Show the average of electrodes in 9 channels
    pl.create_9_evoked_group_plot(sub, AllGrandAverage, conditions_compared, plot_cond_name, plot_compare_erp_path, save, plot)#, colors)

################################## What to run #################################

if __name__ == '__main__' :

    print('Presentation scripts')

    print('MNE VERSION : ', mne.__version__)

    #data_grandaverage_path = './../DELIRIUM_PROJECT/DELIRIUM_ANALYSIS/MATHS_NOBAD/data_grandaverage/'
    data_grandaverage_path = 'G:/Delirium/GitLab/DELIRIUM_PROJECT/DELIRIUM_ANALYSIS/WORDS_PATIENTS_DEL_0.5/data_grandaverage/'
    name = 'GrandAverage.npy'
    all_subjects = data_grandaverage_path + name

    run_on_group(all_subjects)
