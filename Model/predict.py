import torch
import numpy as np
from scipy.signal import resample, welch
import pandas as pd

# This script recieves data from the brainflow code and returns a prediction
# also has functions for welch power spectral density and bandpower

# predict class label
def predict(model, data, device):
    model.eval()
    predictions = []
    with torch.no_grad():
        data = data.to(device)
        output = model(data)
        _, pred = torch.max(output, 1)
        predictions.extend(pred.cpu().numpy())
    return np.array(predictions)

def extract_data(raw):
    # extract eeg signals (1-16 for now needs changing)
    if raw.shape[1] < 750:
        # pad with zeros if needed
        raw = np.concatenate((raw, np.zeros((16, 750 - raw.shape[1]))), axis=1)
    # only take 750 samples (3 seconds)
    data = raw[0:16,:0:750]
    # resample to 480 samples
    return resample(data, 480, axis=1)


#Function gets the mean power of a specified frequency band. Will be used to calculate power estimations of most common frequency bands
def bandpower(data, sf, band, output = False):
    band = np.asarray(band)
    low, high = band

    # Compute the periodogram (Welch)
    freqs, psd = welch(data, 
                       sf, 
                       nperseg=sf,
                       scaling='density', 
                       axis=0)
    
    # put into a df
    psd = pd.DataFrame(psd, index = freqs)
    
    if output:
        print('Welch Output')
        psd.index.name = 'Hz'
        psd.columns = ['Power']
        print(psd)
    
    # Find closest indices of band in frequency vector
    idx_min = np.argmax(np.round(freqs) > low) - 1
    idx_max = np.argmax(np.round(freqs) > high)
    
    # select frequencies of interest
    psd = psd.iloc[idx_min:idx_max,:]
    
    # get the mean of each channel over all frequencies in the band
    psd = psd.mean()
    
    if output:
        print('\nMean Frequency Band')
        print(psd)
    
    return psd

# computes the percentage of power in the beta frequency band (12-30Hz)
def beta_percentage(data, sample_rate):
    beta = bandpower(data, sample_rate, [12,30])
    total = bandpower(data, sample_rate, [0.1,70])
    
    return beta/total

def main(input=False):
    # load model
    model = torch.load('trained_models/model.pth')

    # set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    while input:
        # get data from brainflow
        raw = input()
        # extract data
        data = extract_data(raw)
        # predict
        pred = predict(model, data, device)
        
        # get concentration value
        max_val = 1
        concentration_val = beta_percentage(data, 480) / 1

        # SOCKET TO SEND DATA HERE (pred and concentraion_val)

    return pred