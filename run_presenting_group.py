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

if protocol == 'PP':
    import config_PP as cfg


def run_on_group(all_subjects):


    '''
    Run the analysis on a specific subject
    based on run_on_all_autoreject.py code from Lizette
    '''

    picks = "data" # channel name, or data = GFP
    save = True
    verbose = True
    plot = True 
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
    
    PP = AllGrandAverage['PP']
    AP = AllGrandAverage['AP']

    conditions_compared = [PP, AP]
    plot_cond_name = 'PP_AP'
    
    '''
    
    
    ### ALL THE FIGURES YOU WANT TO SHOW PER SUBJECT ###

    ##show all electrodes:
    pl.create_compare_evoked_group_plot_topo(sub, AllGrandAverage, conditions_compared, plot_cond_name, plot_compare_erp_path, save)

    #pl.create_compare_ERP_plot_topo(sub, AllGrandAverage,conditions_compared, plot_compare_erp_path, save)

    ##Show comparison of electrodes on GFP or an electrode (using picks)
    pl.create_compare_evoked_group_plot(sub, AllGrandAverage, conditions_compared, plot_cond_name, plot_compare_erp_path, picks, save, plot)

    ##Show the average of electrodes in 11 areas
    pl.create_11_evoked_group_plot(sub, AllGrandAverage, conditions_compared, plot_cond_name, plot_compare_erp_path, save, plot)

    ##Show the average of electrodes in 9 channels
    pl.create_9_evoked_group_plot(sub, AllGrandAverage, conditions_compared, plot_cond_name, plot_compare_erp_path, save, plot)#, colors)

################################## What to run #################################

if __name__ == '__main__' :

    print('Presentation scripts')

    print('MNE VERSION : ', mne.__version__)

    data_grandaverage_path = mypath + 'WORDS/data_grandaverage/'
    name = 'GrandAverage.npy'
    all_subjects = data_grandaverage_path + name

    run_on_group(all_subjects)
