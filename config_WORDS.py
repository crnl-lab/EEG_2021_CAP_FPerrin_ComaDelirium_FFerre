import pandas as pd
import numpy as np

'''
Descirption
study:      N400
Protocol:   Delirium
Resp.:       F Perrin
Lead.:       F Ferre
Code:        L Heine - A Corneyllie

this file gives general settings for the study 'N400'

'''
################################### Subjects ###################################

mypath = 'G:/Delirium/GitLab/DELIRIUM_PROJECT/DELIRIUM_ANALYSIS/'

csv_path = mypath + 'WORDS_Tp_DEL.csv'
df = pd.read_csv(csv_path ,sep=",", keep_default_na=False)
all_subjects=[]
id_patient=[]
#group=[]
protocol=[]
type_EEG=[]
bad_sub_chans=[]

def info_subject():
    for i in range(len(df)):
        all_subjects.append(df["nom_fichier"][i]) #sub
        id_patient.append(df["ID_patient"][i])
        bad_sub_chans.append(df["bad_sub_chan"][i])
        protocol.append(df["protocol"][i])
        # this dictionnarry comes from preliminary data visual checking using 'get_bad_chan' function


############################# General definitions ##############################
##folders to store the data (they are expected to excist!)

data_Subject_Dir = mypath + 'data_EEG_patients/'
stimDict_path = mypath + 'WORDS_PATIENTS_DEL_0.5/data_stimdict/'
data_preproc_path = mypath + 'WORDS_PATIENTS_DEL_0.5/data_preproc/'
data_epochs_path = mypath + 'WORDS_PATIENTS_DEL_0.5/data_epochs/'
data_evoked_path = mypath + 'WORDS_PATIENTS_DEL_0.5/data_evoked/'
plot_topo_path = mypath + 'WORDS_PATIENTS_DEL_0.5/plots/Topomap/'
plot_erp_path = mypath + 'WORDS_PATIENTS_DEL_0.5/plots/ERP/'
plot_stats_path = mypath + 'WORDS_PATIENTS_DEL_0.5/plots/stats/'
data_stats_path = mypath + 'WORDS_PATIENTS_DEL_0.5/stats/'
text_stats_path = mypath + 'WORDS_PATIENTS_DEL_0.5/stats/'
cleaning_path = mypath + 'WORDS_PATIENTS_DEL_0.5/plots/cleaning/'
data_grandaverage_path = mypath + 'WORDS_PATIENTS_DEL_0.5/data_grandaverage/'
plot_grandaverage_path = mypath + 'WORDS_PATIENTS_DEL_0.5/plots/grandaverage/'
plot_GFP_path = mypath + 'WORDS_PATIENTS_DEL_0.5/plots/GFP/'

data_evoked_group_path = mypath + 'WORDS_PATIENTS_DEL_0.5/data_evoked_group/'
plot_evoked_group_path = mypath + 'WORDS_PATIENTS_DEL_0.5/plots/evoked_group/'

##Prefixes - how to name the data after each step
prefix_stimDict = '_event_id.npy'
prefix_processed = '_preproc.fif'
prefix_epochs_PPAP = '_WORDS-epo.fif'
prefix_ICA = '_ICA.fif'
prefix_noICA = '_noICA.fif'
prefix_autoreject = '_ar.fif'
prefix_ave = '-erp.fif'
prefix_grandaverage = 'GrandAverage'
prefix_evoked_group = '_evoked_group.fif'


################################ /../General params ################################
proj_name = 'Delirium_WORDS'


########### For Preprossessing
# Band Pass filter  around 1-25Hz
highpass = 0.5
highcut = 25

#exemptions:
#cut in specific place:
i_start_TWB1 = float(0)
i_stop_TWB1 = float(1250)
i_start_TPC2 = float(700)
i_stop_TPC2 = float(2050)


########### For epoching
# Initial rejection setting
epochs_reject=None #dict(eeg= 150e-6, eog=150e-6)

# For blink detection (could be a dict if different params by subjects)
minBlinksICA = 100
eog_threshold = 3
# For ICA'/logs/'
n_components = 0.99  # if float, select n_components by explained variance of PCA
method = 'fastica'  # for comparison with EEGLAB try "extended-infomax" here
decim = 2  # we need sufficient statistics, not all time points -> saves time
random_state = 23
ica_reject = None
erp_reject = {'eeg': 100e-6, 'eog': 200e-6} ## used only during ICA

#for epoching
erp_window_tmin = -0.2
erp_window_tmax = 1
erp_baseline = (None, 0) # from first instance to t=0
erp_detrend = None # None= NO DETREND! Either 0 or 1, the order of the detrending. 0 is a constant (DC) detrend, 1 is a linear detrend.
erp_topo = True


#for stats
alphaClusterP = 0.01 #should be 0.001
p_accept = 0.05 #should be 0,05
permutations = 1000 #should be 10000



################################## ERP params ##################################

## For the stimuli dictionary (names of stimuli given automatically vs ones we gave the stimuli)
nameStimDict = mypath + 'WORDS_PATIENTS_DEL_0.5/data_stimdict/'
nameStim_prefix = 'event_id.npy'

events_id = {'TW/C/1': 2,'TW/C/2': 3,'TW/C/3': 4,'TW/C/4': 5, 'TW/C/5': 6, 'TW/C/6': 7, 'TW/C/7': 8, 'TW/C/8': 9, 'TW/C/9': 10, 'TW/C/10': 11, 'TW/C/11': 12, 'TW/C/12': 13, 'TW/C/13': 14, 'TW/C/14': 15, 'TW/C/15': 16, 'TW/C/16': 17, 'TW/C/17': 18, 'TW/C/18': 19, 'TW/C/19': 20, 'TW/C/20': 21, 'TW/C/21': 22, 'TW/C/22': 23, 'TW/C/23': 24,'TW/C/24': 25, 'TW/C/25': 26, 'TW/C/26': 27, 'TW/C/27': 28, 'TW/C/28': 29, 'TW/C/29': 30, 'TW/C/30': 31, 'TW/C/31': 32, 'TW/C/32': 33, 'TW/C/33': 34, 'TW/C/34': 35,'TW/C/35': 36, 'TW/C/36': 37, 'TW/C/37': 38, 'TW/C/38': 39, 'TW/C/39': 40, 'TW/C/40': 41, 'TW/C/41': 42, 'TW/C/42': 43, 'TW/C/43': 44, 'TW/C/44': 45, 'TW/C/45': 46, 'TW/C/46': 47, 'TW/C/47': 48, 'TW/C/48': 49, 'TW/C/49': 50, 'TW/C/50': 51, 'TW/C/51': 52, 'TW/C/52': 53, 'TW/C/53': 54, 'TW/C/54': 55, 'TW/C/55': 56, 'TW/C/56': 57, 'TW/C/57': 58, 'TW/C/58': 59, 'TW/C/59': 60, 'TW/C/60': 61, 'TW/C/61': 62, 'TW/C/62': 63, 'TW/C/63': 64, 'TW/C/64': 65, 'TW/C/65': 66, 'TW/C/66': 67, 'TW/C/67': 68, 'TW/C/68': 69, 'TW/C/69': 70, 'TW/C/70': 71, 'TW/C/71': 72, 'TW/C/72': 73, 'TW/C/73': 74, 'TW/C/74': 75, 'TW/C/75': 76, 'TW/C/76': 77, 'TW/C/77': 78, 'TW/C/78': 79, 'TW/C/79': 80, 'TW/C/80': 81,
            'TW/I/1': 101, 'TW/I/2': 102,'TW/I/3': 103,'TW/I/4': 104, 'TW/I/5': 105, 'TW/I/6': 106, 'TW/I/7': 107, 'TW/I/8': 108, 'TW/I/9': 109, 'TW/I/10': 110, 'TW/I/11': 111, 'TW/I/12': 112, 'TW/I/13': 113, 'TW/I/14': 114, 'TW/I/15': 115, 'TW/I/16': 116, 'TW/I/17': 117, 'TW/I/18': 118, 'TW/I/19': 119, 'TW/I/20': 120, 'TW/I/21': 121, 'TW/I/22': 122, 'TW/I/23': 123, 'TW/I/24': 124, 'TW/I/25': 125, 'TW/I/26': 126, 'TW/I/27': 127, 'TW/I/28': 128, 'TW/I/29': 129, 'TW/I/30': 130, 'TW/I/31': 131, 'TW/I/32': 132, 'TW/I/33': 133, 'TW/I/34': 134, 'TW/I/35': 135, 'TW/I/36': 136, 'TW/I/37': 137, 'TW/I/38': 138, 'TW/I/39': 139, 'TW/I/40': 140, 'TW/I/41': 141, 'TW/I/42': 142, 'TW/I/43': 143, 'TW/I/44': 144, 'TW/I/45': 145, 'TW/I/46': 146, 'TW/I/47': 147, 'TW/I/48': 148, 'TW/I/49': 149, 'TW/I/50': 150, 'TW/I/51': 151, 'TW/I/52': 152, 'TW/I/53': 153, 'TW/I/54': 154, 'TW/I/55': 155, 'TW/I/56': 156, 'TW/I/57': 157, 'TW/I/58': 158, 'TW/I/59': 159, 'TW/I/60': 160, 'TW/I/61': 161, 'TW/I/62': 162, 'TW/I/63': 163, 'TW/I/64': 164, 'TW/I/65': 165, 'TW/I/66': 166, 'TW/I/67': 167, 'TW/I/68': 168, 'TW/I/69': 169, 'TW/I/70': 170, 'TW/I/71': 171, 'TW/I/72': 172, 'TW/I/73': 173, 'TW/I/74': 174, 'TW/I/75': 175, 'TW/I/76': 176, 'TW/I/77': 177, 'TW/I/78': 178, 'TW/I/79': 179, 'TW/I/80': 180,
            'TPW': 201, 'PPW': 200, 'PC': 1, 'PI': 100
            }


############### Averaging ###############
#all_conditions  = {  'TWC': ["TW/C"],'TWI': ["TW/I"],'TPW': ["TPW"], 'PPW': ["PPW"], 'PC': ["PC"], 'PI': ["PI"]
#                               }
all_conditions  = {  'TWC': ["TW/C"],'TWI': ["TW/I"],'TPW': ["TPW"]
                                }

############### GROUP analysis ###############
## Topo times ###
topo_times = np.arange(0., 1.2, 0.2)
csv_stats_textfile = mypath + 'WORDS_PATIENTS_DEL_0.5/stats/SpatTempTstats_GrandAverage.csv'

##GrandAverage stats
GA_alphaClusterP = 0.01
GA_p_accept = 0.05
