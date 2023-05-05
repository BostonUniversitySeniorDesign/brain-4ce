import copy
import numpy as np
import scipy.signal as signal
import torch

class FilterBank(object):
    # filters the given signal into specific bands using cheby2 iir filtering.
    # returns a 4D array of shape (batch, nChannles, nSamples, nBands)

    def __init__(self, filtbank, fs, filtAllowance=2, axis=1):
        # filterbank is a list of tuples of the form (low, high)
        # fs is the sampling frequency
        # filtAllowance is the transition band width in Hz
        # axis is the axis along which to filter the signal

        self.filtbank = filtbank
        self.fs = fs
        self.filtAllowance = filtAllowance
        self.axis = axis


    def bandpassFilter(self, data, freqband, fs, filtAllowance=2, axis=1, output=False):
        # filters the given signal into a specific band using cheby2 iir filtering

        aStop = 30 #stopband attenuation in dB
        aPass = 3 #passband attenuation in dB
        nFreq = fs/2 #nyquist frequency

        if((freqband[0] - filtAllowance == 0 or freqband[0] is None) and (freqband[1] >= nFreq or freqband[1] is None)):
            # no filtering required
            print("Invalid cutoff frequencies")
            return data
        elif freqband[0] - filtAllowance <= 0 or freqband[0] is None:
            # lowpass filter
            fpass = freqband[1]/nFreq
            fstop = (freqband[1] + filtAllowance)/nFreq
            [N, ws] = signal.cheb2ord(fpass, fstop, aPass, aStop)
            b, a = signal.cheby2(N, aStop, fstop, 'lowpass')

            if output:
                print('Performing low pass filter with cutoff frequency: ' + str(freqband[1]))

        elif (freqband[1] is None) or (freqband[1] + filtAllowance >= nFreq):
            # highpass filter
            fpass = freqband[0]/nFreq
            fstop = (freqband[0] - filtAllowance)/nFreq

            [N, ws] = signal.cheb2ord(fpass, fstop, aPass, aStop)
            b, a = signal.cheby2(N, aStop, fstop, 'highpass')

            if output:
                print('Performing high pass filter with cutoff frequency: ' + str(freqband[0]))

        else:
            #bandpass filter
            fpass = (np.array(freqband)/nFreq).tolist()
            fstop = [(freqband[0] - filtAllowance)/nFreq, (freqband[1] + filtAllowance)/nFreq]

            [N, ws] = signal.cheb2ord(fpass, fstop, aPass, aStop)
            b, a = signal.cheby2(N, aStop, fstop, 'bandpass')

            if output:
                print('Performing band pass filter with frequency band: (' + str(freqband[0]) + ',' + str(freqband[1]) + ')')
        
        dataout = signal.lfilter(b, a, data, axis=axis)
        return dataout
    

    def __call__(self, data, output=False):
        data_copy = copy.deepcopy(data)
        # init output array
        out = np.zeros([*data_copy.shape, len(self.filtbank)])
        # apply filters, append to last dimension
        for i, filtBand in enumerate(self.filtbank):
            out[:,:,:,i] = self.bandpassFilter(data_copy, filtBand, self.fs, self.filtAllowance, self.axis, output)
        
        return torch.from_numpy(out).float()
