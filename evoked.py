import mne
import numpy as np
import matplotlib.pyplot as plt
import os


#import config_protoPPmusic_ConvolutionEGI as cfg
## logging info ###
import logging
from datetime import datetime

logname = './logs/' + datetime.now().strftime('log_%Y-%m-%d.log')
logging.basicConfig(filename=logname,level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)


def create_ERP_egi(epochs, sub_name,fif_fname, protocol, plot=True, save=True):
    if protocol == 'WORDS':
        import config_WORDS as cfg

    if protocol == 'PP':
        import config_PP as cfg


    '''
    This function create evoked data and plots
    It supposes that raw data have been preprocessed and epoked data is saved to a .fif file
    (for exemple in data_preproc & data_erp folder)
    Averaged evoked data is saved in 'data_evoked'
    Figures if created are saved in the plots folders

    '''
    #fif_base_name = epochs_name.split('/')[-1].strip('.fif') + '_'
    fif_base_name = fif_fname.split('/')[-1].strip('.fif')

    condEvokeds = [epochs[con].average() for con in  list(cfg.all_conditions.values())]# ["PP","AP/1","AP/2","AP/3","AP/4","AP/5","AP/6"]] #TODO instead of this link to all_conditions?
    print(condEvokeds)
    for index, con in enumerate(list(cfg.all_conditions)):
        print('index : ',index)
        print('con : ', con)
        condEvokeds[index].comment = con
        '''
        if plot:
            condEvokedFig = condEvokeds[index].plot(spatial_colors=True, titles=title, gfp=True, show=show, exclude='bads') #ylim=dict(eeg=[-10,8]),
            if save:
                png_name = cfg.plot_erp_path +  fif_base_name + con +'.png'
                condEvokedFig.savefig(png_name)
        if topo:
            condTopoFig = condEvokeds[index].plot_topomap(times= np.arange(0,1.2,0.1), ch_type='eeg', show=show, title=title)
            if save:
                png_name = cfg.plot_topo_path +  fif_base_name + con +'.png'
                #print(png_name)
                condTopoFig.savefig(png_name)
        '''

    evoked_dict = dict()

    for con in cfg.all_conditions:

        print('## Condition : ', con)
        logger.info("condition: ,%s", con)
        logger.info("nb events: ,%s", len(epochs[cfg.all_conditions[con]]))
        print("nb events:", len(epochs[cfg.all_conditions[con]]))

        condEvoked = epochs[cfg.all_conditions[con]].average()
        condEvoked.comment = con
        title = sub_name + ' ' + con
        condEvokedFig = condEvoked.plot(spatial_colors=True, titles=title, gfp=True, show=plot, exclude='bads') #ylim=dict(eeg=[-10,8]),
        if save:
            png_name = cfg.plot_erp_path +  fif_base_name + '_' +  con +'.png'
            condEvokedFig.savefig(png_name)
        if cfg.erp_topo:
            condTopoFig = condEvoked.plot_topomap(times= np.arange(0,0.8,0.1), ch_type='eeg', show=plot, title=title)
            if save:
                png_name = cfg.plot_topo_path +  fif_base_name + '_' +  con +'.png'
                #print(png_name)
                condTopoFig.savefig(png_name)


    if save:
        AllConditions_name = cfg.data_evoked_path + fif_base_name + cfg.prefix_ave
        print(AllConditions_name)
        mne.write_evokeds(AllConditions_name, condEvokeds)
        logger.info('Saved evoked (ERP) datafile', AllConditions_name)

    return condEvokeds


def create_ERP_PPAP_mircomed(epochs, sub_name,fif_fname, plot=True, save=True):
    import config_protoPPmusic_micromed as cfg
    '''
    This function create evoked data and plots
    It supposes that raw data have been preprocessed and epoked data is saved to a .fif file
    (for exemple in data_preproc & data_erp folder)
    Averaged evoked data is saved in 'data_evoked'
    Figures if created are saved in the plots folders

    '''
    #fif_base_name = epochs_name.split('/')[-1].strip('.fif') + '_'
    fif_base_name = fif_fname.split('/')[-1].strip('.fif')

    condEvokeds = [epochs[con].average() for con in  list(cfg.all_conditions.values())]# ["PP","AP/1","AP/2","AP/3","AP/4","AP/5","AP/6"]] #TODO instead of this link to all_conditions?
    print(condEvokeds)
    for index, con in enumerate(list(cfg.all_conditions)):
        print('index : ',index)
        print('con : ', con)
        condEvokeds[index].comment = con
        '''
        if plot:

            condEvokedFig = condEvokeds[index].plot(spatial_colors=True, titles=title, gfp=True, show=show, exclude='bads') #ylim=dict(eeg=[-10,8]),
            if save:
                png_name = cfg.plot_erp_path +  fif_base_name + con +'.png'
                condEvokedFig.savefig(png_name)
        if topo:
            condTopoFig = condEvokeds[index].plot_topomap(times= np.arange(0,1.2,0.1), ch_type='eeg', show=show, title=title)
            if save:
                png_name = cfg.plot_topo_path +  fif_base_name + con +'.png'
                #print(png_name)
                condTopoFig.savefig(png_name)
        '''

    evoked_dict = dict()

    for con in cfg.all_conditions:

        print('## Condition : ', con)
        logger.info("condition: ,%s", con)
        logger.info("nb events: ,%s", len(epochs[cfg.all_conditions[con]]))
        print("nb events:", len(epochs[cfg.all_conditions[con]]))

        condEvoked = epochs[cfg.all_conditions[con]].average()
        condEvoked.comment = con
        title = sub_name + ' ' + con
        condEvokedFig = condEvoked.plot(spatial_colors=True, titles=title, gfp=True, show=plot, exclude='bads') #ylim=dict(eeg=[-10,8]),
        if save:
            png_name = cfg.plot_erp_path +  fif_base_name + '_' + con +'.png'
            condEvokedFig.savefig(png_name)
        if cfg.erp_topo:
            condTopoFig = condEvoked.plot_topomap(times= np.arange(0,0.8,0.1), ch_type='eeg', show=plot, title=title)
            if save:
                png_name = cfg.plot_topo_path +  fif_base_name + '_' + con +'.png'
                #print(png_name)
                condTopoFig.savefig(png_name)
    #plt.show()


    if save:
        AllConditions_name = cfg.data_evoked_path + fif_base_name + cfg.prefix_ave
        print(AllConditions_name)
        mne.write_evokeds(AllConditions_name, condEvokeds)
        #logger.info('Saved evoked (ERP) datafile', AllConditions_name)

    return condEvokeds
