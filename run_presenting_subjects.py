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

########### Setup for logging ################
protocol = 'WORDS'

if protocol == 'WORDS':
    import config_WORDS as cfg

if protocol == 'PP':
    import config_PP as cfg

def run_on_subjects(all_subjects):

    '''
    Run the analysis on a specific subject
    based on run_on_all_autoreject.py code from Lizette
    '''

    ## CHOOSE CONDITIONS, COLORS, LINESTYLES

    conditions_compared = ["TWC", "TWI", "TPW"] ##Can be as many conditions as you want
    #conditions_compared = ["PP", "AP"]

    #colors = {"TWC": "skyblue", "TWI": "slategray", "TPW": "black"}
    #colors = {"PP": "skyblue", "AP": "slategray"}

    picks =  "data" # channel name (e.g., E30), or data = GFP
    save = True
    verbose = False
    plot = True
    plot_compare_erp_path = cfg.plot_GFP_path ## TO ADD OR CHANGE, make clear folders
    data_evoked_path = cfg.data_evoked_path


    for sub_number, sub in enumerate(all_subjects, start=0):
        print("Working on " + sub)

        listdir=[]
        for filename in os.listdir(data_evoked_path):
            print(sub )
            print(filename)
            if fnmatch.fnmatch(filename, sub + cfg.prefix_processed.strip('.fif') + '*' + cfg.prefix_ave):
                print(filename)
                listdir.append(filename)
                print(listdir)
        if len(listdir) == 1:
            evoked_name = cfg.data_evoked_path + listdir[0]
            print(evoked_name)

            ### ALL THE FIGURES YOU WANT TO SHOW PER SUBJECT ###

            ##show all electrodes:
            pl.create_compare_ERP_plot_topo(sub, evoked_name, conditions_compared, plot_compare_erp_path, save)

            ##Show comparison of electrodes on GFP or ERP for an electrode (using picks)
            pl.create_compare_ERP_plot(sub, evoked_name, conditions_compared, plot_compare_erp_path, picks, save, plot)

            ##Show the plot of the difference between two conditions
            #pl.create_difference_ERP_plot(sub, evoked_name, conditions_compared, plot_compare_erp_path, save, plot) ## have only 2 conditions_compared, or it takes the first two in the list

            ##Show the average of electrodes in 11 areas
            pl.create_11_erp_plot(sub, evoked_name, conditions_compared, plot_compare_erp_path, save, plot)
            
            ##Show the average of electrodes in 9 channels
            pl.create_9_erp_plot(sub, evoked_name, conditions_compared, plot_compare_erp_path, save, plot)

        else:
            print('ERROR: multiple or no files found, problem in analysis for subject: ' + sub)
            print(listdir)
            exit()



################################## What to run #################################

if __name__ == '__main__' :

    print('Presentation scripts')

    print('MNE VERSION : ', mne.__version__)

    all_subjects = ['Subject1_WORDS', 'Subject2_WORDS', 'Subject3_WORDS']
    #all_subjects = ['Subject1_PP', 'Subject2_PP', 'Subject3_PP']


    run_on_subjects(all_subjects)
