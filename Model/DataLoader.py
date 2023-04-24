from mne.datasets import eegbci
from torch.utils.data import Dataset, DataLoader, TensorDataset
from mne.io import concatenate_raws, read_raw_edf
import mne
import numpy as np
import torch



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


# Load eegbci data for a given subject list defined by subjects
# channels is a list of channels to extract in range (0,63)
def load_eegbci_data(subjects, channels, data_path):
    data = []
    labels = []
    cases = [[3,4,7,8,11,12], [1,2,5,6,9,10,13,14]]

    for channel in channels:
        if channel < 0 or channel > 63:
            raise ValueError("Channel number must be between 0 and 63")

    for subject in subjects:
        
        if subject < 1 or subject > 109:
            raise ValueError("Subject number must be between 1 and 109")
        
        epochs_case1 = create_epochs(subject, cases[0], data_path)
        epochs_case2 = create_epochs(subject, cases[1], data_path)

        for curr_epoch in [epochs_case1, epochs_case2]:
            data.append(curr_epoch['T2']._data[:, channels, :])
            data.append(curr_epoch['T1']._data[:, channels, :])
            data.append(curr_epoch['T0']._data[:, channels, :])

        # Class, Action
        # 0, Rest
        # 1, Right fist
        # 2, Left fist
        # 3, Both fists
        # 4, Both feet

        labels.append(np.full((1,len(epochs_case1['T0']._data)),0))
        labels.append(np.full((1,len(epochs_case1['T1']._data)),2))
        labels.append(np.full((1,len(epochs_case1['T2']._data)),1))
        labels.append(np.full((1,len(epochs_case2['T0']._data)),0))
        labels.append(np.full((1,len(epochs_case2['T1']._data)),3))
        labels.append(np.full((1,len(epochs_case2['T2']._data)),4))

    data = np.concatenate(data, axis=0)
    labels = np.concatenate(labels, axis=1)
    labels = labels[0]

    # Convert data and labels to PyTorch tensors
    data = torch.from_numpy(data).float()
    labels = torch.from_numpy(labels).long()

    return data, labels

def PhysionetDataLoader(subjects, channels, datapath, batch_size, shuffle=True):
    data, labels = load_eegbci_data(subjects, channels, datapath)
    dataset = TensorDataset(data, labels)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)