import numpy as np
import pandas as pd
'''
Descirption
study:      EEG music convolution study
Protocol:   Coma PP music
Resp.:       F Perrin
Lead.:       L Heine
Code:        L Heine - A Corneyllie

this file gives general settings for the study 'Early Evocked'

'''

################################### Subjects ###################################

my_path = 'H:/Delirium/GitLab/DELIRIUM_PROJECT/DELIRIUM_ANALYSIS/'

csv_path = my_path + 'PP.csv'
df = pd.read_csv(csv_path ,sep=",", keep_default_na=False)
all_subjects=[]
id_patient=[]
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
data_Subject_Dir = my_path + 'data_EEG_patients/'
stimDict_path = my_path + 'PP/data_stimdict/'
data_preproc_path = my_path + 'PP/data_preproc/'
data_epochs_path = my_path + 'PP/data_epochs/'
data_evoked_path = my_path + 'PP/data_evoked/'
plot_topo_path = my_path + 'PP/plots/Topomap/'
plot_erp_path = my_path + 'PP/plots/ERP/'
plot_stats_path = my_path + 'PP/plots/stats/'
data_stats_path = my_path + 'PP/stats/'
text_stats_path = my_path + 'PP/stats/'
cleaning_path = my_path + 'PP/plots/cleaning/'
data_grandaverage_path = my_path + 'PP/data_grandaverage/'
plot_grandaverage_path = my_path + 'PP/plots/grandaverage/'
plot_GFP_path = my_path + 'PP/plots/GFP/'

data_evoked_group_path = my_path + 'PP_TpAP/data_evoked_group/'
plot_evoked_group_path = my_path + 'PP_TpAP/plots/evoked_group/'


##Prefixes - how to name the data after each step
prefix_stimDict = '_event_id.npy'
prefix_processed = '_preproc.fif'
prefix_epochs_PPAP = '_PP-epo.fif'
prefix_ICA = '_ICA.fif'
prefix_noICA = '_noICA.fif'
prefix_autoreject = '_ar.fif'
prefix_ave = '-erp.fif'
prefix_grandaverage = 'GrandAverage'
prefix_evoked_group = '_evoked_group.fif'


################################ /../General params ################################
proj_name = 'Delirium_PP'


########### For Preprossessing
# Band Pass filter  around 1-25Hz
highpass = 0.5
highcut = 25


########### For epoching
# Initial rejection setting
epochs_reject=None #dict(eeg= 150e-6, eog=150e-6)

# For blink detection (could be a dict if different params by subjects)
minBlinksICA = 100  #300 for protocol PP Lizette
eog_threshold = 3
# For ICA
n_components = 0.99  # (instead of 0.95) if float, select n_components by explained variance of PCA
method = 'fastica'  # for comparison with EEGLAB try "extended-infomax" here
decim = 2  # we need sufficient statistics, not all time points -> saves time
random_state = 23
ica_reject = None
erp_reject = {'eeg': 100e-6, 'eog': 200e-6}

#for epoching
erp_window_tmin = -0.2
erp_window_tmax = 1
erp_baseline = (None, 0) # from first instance to t=0
erp_detrend = None # Either 0 or 1, the order of the detrending. 0 is a constant (DC) detrend, 1 is a linear detrend.
erp_topo = True


#for stats
alphaClusterP = 0.01 #could be 0.001
p_accept = 0.05 
permutations = 1000 #could be 10000



################################## ERP params ##################################

## For the stimuli dictionary (names of stimuli given automatically vs ones we gave the stimuli)
nameStimDict = my_path + 'PP/data_stimdict/'
#nameStimDict = './PP/data_stimdict/'
nameStim_prefix = 'event_id.npy'

events_id = { 'PP/10': 110,'PP/20': 120,'PP/30': 130, 'AP/11': 111, 'AP/12': 112, 'AP/13': 113, 'AP/14': 114, 'AP/15': 115, 'AP/16': 116,
'AP/21': 121, 'AP/22': 122, 'AP/23': 123, 'AP/24': 124, 'AP/25': 125, 'AP/26': 126,
'AP/31': 131, 'AP/32': 132, 'AP/33': 133, 'AP/34': 134, 'AP/35': 135, 'AP/36': 136 } #'AP/22': 108, 'AP/12': 4 pour TpJC5 qui a 2 triggers en trop (22 et 23 devenus 4 et 108)


############### Averaging ###############
'''
all_conditions  = { 'SON' : ["PP/10","PP/20","PP/30"],
                    'OFN' : ["AP/11","AP/12","AP/13","AP/14","AP/15","AP/16","AP/21", "AP/22","AP/23","AP/24","AP/25","AP/26","AP/31","AP/32","AP/33","AP/34","AP/35","AP/36"]
                    }
'''

all_conditions  = { 'PP' : ["PP"],
                    'AP' : ["AP"],
                    }

############### GROUP analysis ###############
## Topo times ###
topo_times = np.arange(0., 1.2, 0.2)

csv_stats_textfile = my_path + 'PP/stats/SpatTempTstats_GrandAverage.csv'

##GrandAverage stats
GA_alphaClusterP = 0.01
GA_p_accept = 0.05

#Best Team Ever Lizette/Fabrice/Alex <3
