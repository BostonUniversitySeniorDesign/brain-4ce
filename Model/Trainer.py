from DataLoader import *
from FBCNetwork import *
from Filter import FilterBank

import torch
import torch.nn as nn
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from csv import writer


class FBCTrainer:

    def __init__(self, network, channels, batch_size, fs, datapath, savepath):
        self.channels = channels
        self.datapath = datapath
        self.fs = fs
        self.batch_size = batch_size
        self.filterbank = FilterBank([(4,8), (8, 12), (12, 16), (16,20), (20,24), (24,28), (28,32), (32,36), (36,40)], fs=fs, axis=2) 
        self.network = network
        self.savepath = savepath

        # split subject list into train and test
        # not ideal due to subject bias but will do for now
        subjects = np.arange(1, 109)
        self.train_subjects, self.test_subjects = train_test_split(subjects, test_size=0.2, random_state=42)


    def transform(self, data, filter=True, convert_unit=True, output=False):
        # convert data to microvolts
        if(convert_unit):
            data = data * 1e6
        # apply filters on data
        if(filter):
            data = self.filterbank(data, output)
        return data

    def train(self, device, optimizer, criterion, nEpochs=100):
        self.network.to(device)
        self.network.train()
        losses = []
        accuracies = []
        for epoch in range(nEpochs):
            preds_epoch = []
            labels_epoch = []
            losses_epoch = []
            # load subject data one at atime
            for subject in self.train_subjects:
                loader = PhysionetDataLoader([subject], self.channels, self.datapath, batch_size=self.batch_size, shuffle=False)
                for i, (data, labels) in enumerate(loader):
                    # apply filters on data
                    transformed_data = self.transform(data, filter=True, convert_unit=True, output=False)
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
                    # track losses and accuracy for each epoch
                    _, predicted = torch.max(output.data, 1)
                    preds_epoch = np.concatenate((preds_epoch, predicted.data.cpu().numpy()), axis=0)
                    labels_epoch = np.concatenate((labels_epoch, labels.data.cpu().numpy()), axis=0)
                    losses_epoch.append(loss.item())

            # calculate accuracy
            total = len(labels_epoch)
            correct = np.sum(np.array(preds_epoch) == np.array(labels_epoch))
            accuracy = correct / total
            accuracies.append(accuracy)
            losses.append(np.mean(losses_epoch))
            print('Epoch: {} | Loss: {} | Accuracy: {}'.format(epoch, np.mean(losses_epoch), accuracy))

            if epoch % 10 == 0 and self.savepath != None:
                self.save_network(epoch, 'FBC', self.savepath)
                results_path = os.path.join(self.savepath, 'results.csv')
                # save results to csv
                with open(results_path, 'a') as f:
                    writer_obj = writer(f)
                    writer_obj.writerow([epoch, np.mean(losses_epoch), accuracy])
                    f.close()

        return losses, accuracies


    def test(self, device, criterion):
        self.network.to(device)
        self.network.eval()
        preds_epoch = []
        labels_epoch = []
        losses_epoch = []
        # load subject data one at atime
        for subject in self.test_subjects:
            loader = PhysionetDataLoader([subject], self.channels, self.datapath, batch_size=self.batch_size, shuffle=False)
            for i, (data, labels) in enumerate(loader):
                # apply filters on data
                transformed_data = self.transform(data, filter=True, convert_unit=True, output=False)
                # forward pass
                output = self.network(transformed_data.to(device))
                # reformat labels
                labels = labels.type(torch.LongTensor).to(device)
                # calculate loss
                loss = criterion(output, labels)                    
                # track losses and accuracy for each epoch
                _, predicted = torch.max(output.data, 1)
                preds_epoch = np.concatenate((preds_epoch, predicted.data.cpu().numpy()), axis=0)
                labels_epoch = np.concatenate((labels_epoch, labels.data.cpu().numpy()), axis=0)
                losses_epoch.append(loss.item())

        # calculate accuracy
        total = len(labels_epoch)
        correct = np.sum(np.array(preds_epoch) == np.array(labels_epoch))
        accuracy = correct / total
        print('Test Accuracy: {}'.format(accuracy))
        cm = confusion_matrix(np.array(labels_epoch), np.array(preds_epoch))
        print(cm)
        # append test accuracy to results csv
        if self.savepath != None:
            results_path = os.path.join(self.savepath, 'results.csv')
            with open(results_path, 'a') as f:
                        writer_obj = writer(f)
                        writer_obj.writerow(['test', np.mean(losses_epoch), accuracy])
                        f.close()
        return accuracy, cm


    def save_network(self,  epoch, name, savepath):
        #Define model name, and save path
        model_name = 'epoch_{}_{:03d}.pth'.format(name, epoch)
        savepath = os.path.join(savepath, model_name)
        # Convert state_dict to cpu
        state_dict = self.network.state_dict()
        for key, param in state_dict.items():
            state_dict[key] = param.cpu()

        #Save model
        torch.save(state_dict, savepath)