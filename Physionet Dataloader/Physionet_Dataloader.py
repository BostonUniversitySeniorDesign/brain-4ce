#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import idx2numpy
import numpy as np
import mne
import argparse
import os
from mne.datasets import eegbci
from mne.io import concatenate_raws, read_raw_edf


parser = argparse.ArgumentParser()
parser.add_argument("-d", type=int, choices=[2, 3], default=3, help="choose a value of 2 or 3 for the -d flag (default: 3)")
parser.add_argument("--data_path", type=str, required=False, default=None, help="path to the data file")
parser.add_argument("--save_path", type=str, required=False, default=None, help="path to save the output file")

args = parser.parse_args()

#This function loads the EEG BCI Data and formats it into a dictionary that can be indexed by the task number (T0, T1, T2) with values formatted as a num_samples X 64 X 961(timesteps) ndarray
# @params
# Subject: Subject number to extract data from
# Cases an array-like object that contains which experiments to extract (1-14)
# @returns:
# epoch containing data from subject in each case of cases
def create_epochs(subject, cases, datapath):
    #Load data
    files = eegbci.load_data(subject, cases, datapath)
    # Convert to raw object
    raws = [read_raw_edf(f, preload=True) for f in files]
    #Combine all loaded runs
    raw_obj = concatenate_raws(raws)
    #Get Events
    events, event_ids = mne.events_from_annotations(raw_obj, event_id='auto')
    #Set epoch size
    tmin, tmax = -1, 4
    #Create epoch map
    epochs = mne.Epochs(raw_obj, events, event_ids, tmin - 0.5, tmax + 0.5, baseline=None, preload=True)
    return epochs

#for cases group 1 T2 represents right fist and T1 represents left fist
#for cases group 2 T2 represents both feet and T1 represents both fists
#for both T0 represtents rest
cases_1 = [3,4,7,8,11,12]
cases_2 = [1,2,5,6,9,10,13,14]


if(args.data_path is None):
    datapath = 'C:\\Users\\shortallb\\Documents\\brain-4ce\\PCA\\Data\\'
else:
    datapath = args.data_path

epochs_case1 = create_epochs(1, cases_1, datapath)
epochs_case2 = create_epochs(1, cases_2, datapath)

#Compute for 10 subjects
for subject in range(2,10):
    #Create epochs for current subject
    epoch_curr_1 = create_epochs(subject, cases_1, datapath)
    epoch_curr_2 = create_epochs(subject, cases_2, datapath)
    #Concatenate to total dataset
    epochs_case1 = mne.concatenate_epochs([epochs_case1, epoch_curr_1])
    epochs_case2 = mne.concatenate_epochs([epochs_case1, epoch_curr_2])

total_data = np.concatenate((epochs_case1['T2']._data, epochs_case1['T1']._data, epochs_case1['T0']._data, 
                             epochs_case2['T2']._data, epochs_case2['T1']._data, epochs_case2['T0']._data),
                            axis=0)
labels = np.concatenate((np.full((1,len(epochs_case1['T0']._data)),6), np.full((1,len(epochs_case1['T1']._data)),0), np.full((1,len(epochs_case1['T2']._data)),2),
                         np.full((1,len(epochs_case2['T0']._data)),6), np.full((1,len(epochs_case2['T1']._data)),1), np.full((1,len(epochs_case2['T2']._data)),4) ), axis=1 )
labels = labels[0]


if(args.save_path is None):
    savepath = 'C:\\Users\\shortallb\\Documents\\brain-4ce\\PCA\\Data\\'
else:
    savepath = args.save_path

# args.d = 2 if we want to save in 2D format, else save in 3D format
if(args.d == 2):
    labels_2D = np.concatenate((np.full((1,64*len(epochs_case1['T0']._data)),6), np.full((1,64*len(epochs_case1['T1']._data)),0), np.full((1,64*len(epochs_case1['T2']._data)),2),
                            np.full((1,64*len(epochs_case2['T0']._data)),6), np.full((1,64*len(epochs_case2['T1']._data)),1), np.full((1,64*len(epochs_case2['T2']._data)),4) ), axis=1 )

    labels_2D = labels_2D[0]
    df = pd.DataFrame(labels_2D)
    df.to_csv(os.path.join(savepath, 'labels_2D.csv'))

    # Reshape data to 2D for PCA
    data_2D = np.swapaxes(total_data, 1, 2)
    data_2D = np.reshape(data_2D, (961*3228, 64))
    df = pd.DataFrame(data_2D)
    df.to_csv(os.path.join(savepath, 'data_2D.csv'))
else:
    #Save to idx file to maintain 3 dimensional shape
    idx2numpy.convert_to_file(os.path.join(savepath, 'FormattedPhysionetData.idx'), total_data)
    df = pd.DataFrame(labels)
    df.to_csv(os.path.join(savepath, 'labels_3D.csv'))