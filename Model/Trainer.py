from DataLoader import *
from FBCNetwork import *
from Filter import FilterBank

import torch
import torch.nn as nn
import os
from sklearn.model_selection import train_test_split


class FBCTrainer:

    def __init__(self,  channels, batch_size, fs, datapath, savepath, pretrained=False, load_path=None):
        self.channels = channels
        self.datapath = datapath
        self.fs = fs
        self.batch_size = batch_size
        self.filterbank = FilterBank([(4,8), (8, 12), (12, 16), (16,20), (20,24), (24,28), (28,32), (32,36), (36,40)], fs=fs, axis=2) 

        if(pretrained and load_path != None):
            self.network = torch.load(load_path)
        else:
            self.network = FBCNet(nTime=460, nChan=len(self.channels), nClass=5, nBands=len(self.filterbank), m=32, strideFactor=4, doWeightNorm=True)

        # split subject list into train and test
        # not ideal due to subject bias but will do for now
        subjects = np.arange(1, 109)
        self.train_subjects, self.test_subjects = train_test_split(subjects, test_size=0.2, random_state=42)


    def transform(self, data, filter=True, convert_unit=True):
        # convert data to microvolts
        if(convert_unit):
            data = data * 1e6
        # apply filters on data
        if(filter):
            data = self.filterbank(data, output=True)
        return data

    def train(self, device, optimizer, criterion, lr, nEpochs=100, save=True):
        self.network.train()
        losses = []
        accuracies = []
        for epoch in range(nEpochs):
            # load subject data one at atime
            for subject in self.train_subjects:
                loader = PhysionetDataLoader([subject], self.channels, self.datapath, batch_size=self.batch_size, shuffle=False)
                for i, (data, labels) in enumerate(loader):
                    # apply filters on data
                    transformed_data = self.transform(data, filter=True, convert_unit=True)
                    optimizer.zero_grad()
                    # forward pass
                    output = self.network(transformed_data.to(device))
                    # reformat labels
                    labels = labels.type(torch.LongTensor).to(device)
                    # calculate loss
                    loss = criterion(output, labels)                    
                    #backward pass
                    loss.backward()
                    optimizer.step()

                    if epoch % 10 == 0:
                        # calculate accuracy
                        _, predicted = torch.max(output.data, 1)
                        total = labels.size(0)
                        correct = (predicted == labels).sum().item()
                        accuracy = correct / total
                        accuracies.append(accuracy)
                        losses.append(loss.item())
                        print('Epoch: {} | Loss: {} | Accuracy: {}'.format(epoch, loss.item(), accuracy))


    def save_network(self,  epoch, name, save_path):
        #Define model name, and save path
        model_name = 'epoch_{}_{:03d}.pth'.format(name, epoch)
        save_path = os.path.join(save_path, model_name)
        # Convert state_dict to cpu
        state_dict = self.network.state_dict()
        for key, param in state_dict.items():
            state_dict[key] = param.cpu()

        #Save model
        torch.save(state_dict, save_path)