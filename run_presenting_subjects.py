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
protocol = 'LG'

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

    #conditions_compared = ["TWC", "TWI", "TPW"] ##Can be as many conditions as you want
    #conditions_compared = ["TRUE", "FALSE"]
    #conditions_compared = ["PP", "AP"]
    #conditions_compared = ["LS", "LD", "GS", "GD"]
    #conditions_compared = ["LS", "LD"]
    conditions_compared = ["GS", "GD"]

    #colors = {"TWC": "skyblue", "TWI": "slategray", "TPW": "black"}
    #colors = {"TRUE": "skyblue", "FALSE": "slategray"}
    #colors = {"PP": "skyblue", "AP": "slategray"}
    #colors = {"LS": "skyblue", "LD": "slategray", "GS": "yellowgreen", "GD": "black"}

    #linestyles = {"PP/Conv":'-', "PP/Dio":'-', "AP/Conv":':', "AP/Dio":':'}
    #colors = {"TWC": "skyblue", "TWI": "slategray", "TPW": "black"}
    picks =  "data" # channel name (e.g. E30), or data = GFP
    save = True
    verbose = False
    plot = False
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
            # TODO: FABRICE: CHECK IF ALL ELECTRODES ARE IN THE 11 PLOT script => checked by FABRICE 09292020

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

    #all_subjects = ['TWB1_LG', 'TPC2_LG', 'TJL3_LG', 'TJR7_LG', 'TLP8_LG', 'TPLV4_LG', 'TTDV5_LG', 'LAB1_LG', 'LCM2_LG', 'LAT3_LG', 'LBM4_LG', 'LPO5_LG', 'LAG6_LG', 'TYS6_LG']
    #all_subjects = ['TYS6_WORDS', 'TJL3_WORDS', 'TJR7_WORDS', 'TLP8_WORDS', 'TPLV4_WORDS', 'TTDV5_WORDS', 'LAB1_WORDS', 'LCM2_WORDS', 'LAT3_WORDS', 'LBM4_WORDS', 'LPO5_WORDS', 'LAG6_WORDS', 'TWB1_WORDS', 'TPC2_WORDS']
    #all_subjects = ['TWB1_MATHS', 'TPC2_MATHS', 'TYS6_MATHS', 'TJL3_MATHS', 'TJR7_MATHS', 'TLP8_MATHS', 'TPLV4_MATHS', 'TTDV5_MATHS', 'LAB1_MATHS', 'LCM2_MATHS', 'LAT3_MATHS', 'LBM4_MATHS', 'LPO5_MATHS', 'LAG6_MATHS']
    #all_subjects = ['TYS6_PP', 'TJL3_PP', 'TJR7_PP', 'TLP8_PP', 'TPLV4_PP', 'TTDV5_PP', 'LAB1_PP', 'LCM2_PP', 'LAT3_PP', 'LBM4_PP', 'LPO5_PP', 'LAG6_PP']

    #all_subjects = ['TpCF1_MATHS', 'TpDRL3_MATHS', 'TpMM4_MATHS', 'TpJC5_MATHS', 'TpCB15_MATHS', 'TpJLR17_MATHS', 'TpAB19_MATHS', 'TpPC21_MATHS', 'TpAK24_MATHS', 'TpJB25_MATHS', 'TpJB26_MATHS', 'TpAK27_MATHS', 'TpLA28_MATHS', 'TpPM14_MATHS', 'TpPM31_MATHS']
    #all_subjects = ['TpCF1_PP', 'TpDRL3_PP', 'TpMM4_PP', 'TpJC5_PP', 'TpCB15_PP', 'TpJLR17_PP', 'TpAB19_PP', 'TpPC21_PP', 'TpAK24_PP', 'TpJB25_PP', 'TpJB26_PP', 'TpAK27_PP', 'TpLA28_PP', 'TpPM14_PP', 'TpRD38_PP', 'TpMN42_PP', 'TpMB45_PP', 'TpKT33_PP', 'TpSM49_PP', 'TpAG51_PP', 'TpJPS55_PP']
    #all_subjects = ['TpCF1_MATHS', 'TpDRL3_MATHS', 'TpJC5_MATHS', 'TpJLR17_MATHS', 'TpAK24_MATHS', 'TpJB25_MATHS', 'TpJB26_MATHS', 'TpAK27_MATHS', 'TpLA28_MATHS', 'TpPM14_MATHS', 'TpPM31_MATHS']
    all_subjects = ['TpCF1_LG', 'TpDRL3_LG', 'TpMM4_LG', 'TpJC5_LG', 'TpCB15_LG','TpJLR17_LG', 'TpPC21_LG','TpJB25_LG', 'TpJB26_LG', 'TpAK27_LG', 'TpLA28_LG', 'TpPM14_LG', 'TpPM31_LG', 'TpRD38_LG', 'TpMN42_LG', 'TpMB45_LG', 'TpSM49_LG', 'TpJPS55_LG']
    #all_subjects = ['TpCF1_WORDS', 'TpDRL3_WORDS', 'TpMM4_WORDS', 'TpJC5_WORDS', 'TpCB15_WORDS', 'TpJLR17_WORDS', 'TpAB19_WORDS', 'TpPC21_WORDS', 'TpAK24_WORDS', 'TpJB25_WORDS', 'TpJB26_WORDS', 'TpAK27_WORDS', 'TpLA28_WORDS', 'TpPM14_WORDS', 'TpPM31_WORDS', 'TpRD38_WORDS', 'TpMN42_WORDS', 'TpMB45_WORDS', 'TpKT33_WORDS', 'TpSM49_WORDS', 'TpAG51_WORDS', 'TpJPS55_WORDS']
    #all_subjects = ['TpKT33_WORDS', 'TpSM49_WORDS', 'TpAG51_WORDS', 'TpJPS55_WORDS']

    #all_subjects = ['TpDD2_MATHS', 'TpKS6_MATHS', 'TpJPG7_MATHS', 'TpGB8_MATHS', 'TpMA9_MATHS', 'TpJPL10_MATHS', 'TpLP11_MATHS', 'TpMD13_MATHS', 'TpBD16_MATHS', 'TpJA20_MATHS', 'TpME22_MATHS', 'TpAC23_MATHS', 'TpJCD29_MATHS', 'TpSD30_MATHS', 'TpGT32_MATHS', 'TpFF34_MATHS', 'TpPA35_MATHS', 'TpCG36_MATHS', 'TpRK39_MATHS', 'TpYB41_MATHS', 'TpAM43_MATHS', 'TpPI46_MATHS']
    #all_subjects = ['TpBL47_MATHS', 'TpPL48_MATHS', 'TpRB50_MATHS', 'TpMD52_MATHS', 'TpFL53_MATHS']
    #all_subjects = ['TpKT33_MATHS', 'TpSM49_MATHS', 'TpJPS55_MATHS']
    #all_subjects = ['TpKS6_MATHS', 'TpJPG7_MATHS', 'TpGB8_MATHS', 'TpJPL10_MATHS', 'TpLP11_MATHS', 'TpBD16_MATHS', 'TpME22_MATHS', 'TpAC23_MATHS', 'TpSD30_MATHS']
    #all_subjects = ['TpKS6_LG', 'TpJPG7_LG', 'TpGB8_LG', 'TpJPL10_LG', 'TpLP11_LG', 'TpMD13_LG', 'TpBD16_LG', 'TpJA20_LG', 'TpME22_LG', 'TpAC23_LG', 'TpSD30_LG', 'TpPA35_LG', 'TpCG36_LG', 'TpRK39_LG', 'TpYB41_LG', 'TpAM43_LG', 'TpPI46_LG', 'TpBL47_LG', 'TpPL48_LG', 'TpFL53_LG']
    #all_subjects = ['TpKS6_WORDS', 'TpJPG7_WORDS', 'TpGB8_WORDS', 'TpJPL10_WORDS', 'TpLP11_WORDS', 'TpBD16_WORDS', 'TpJA20_WORDS', 'TpME22_WORDS', 'TpAC23_WORDS', 'TpJCD29_WORDS', 'TpSD30_WORDS', 'TpGT32_WORDS', 'TpFF34_WORDS', 'TpPA35_WORDS', 'TpCG36_WORDS', 'TpRK39_WORDS', 'TpYB41_WORDS', 'TpAM43_WORDS', 'TpPI46_WORDS', 'TpBL47_WORDS', 'TpPL48_WORDS', 'TpRB50_WORDS', 'TpMD52_WORDS', 'TpFL53_WORDS']
    #all_subjects = ['TpKS6_PP', 'TpJPG7_PP', 'TpGB8_PP', 'TpJPL10_PP', 'TpLP11_PP', 'TpMD13_PP', 'TpBD16_PP', 'TpJA20_PP', 'TpME22_PP', 'TpAC23_PP', 'TpSD30_PP', 'TpGT32_PP', 'TpFF34_PP', 'TpPA35_PP', 'TpCG36_PP', 'TpRK39_PP', 'TpYB41_PP', 'TpAM43_PP', 'TpPI46_PP', 'TpBL47_PP', 'TpPL48_PP', 'TpRB50_PP', 'TpMD52_PP', 'TpFL53_PP']
    #all_subjects = ['TpBL47_WORDS', 'TpPL48_WORDS', 'TpRB50_WORDS', 'TpMD52_WORDS', 'TpFL53_WORDS']
    #all_subjects = ['TpDT_PP']
    #all_subjects = ['TpAP_LG']

    run_on_subjects(all_subjects)
