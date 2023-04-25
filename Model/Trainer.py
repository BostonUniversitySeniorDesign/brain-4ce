from DataLoader import *
from FBCNetwork import *
import torch
import torch.nn as nn


class FBCTrainer:

    def __init__(self, device, channels, datapath, savepath, pretrained=False, load_path=None):
        self.device = device
        self.channels = channels
        self.datapath = datapath
        
        if(pretrained and load_path != None):
            self.network = torch.load(load_path)
        else:
            self.network = FBCNet(nTime=961)

    def train(self):
        # load subject data one at atime
        for subject in range(1, 109):
            loader = PhysionetDataLoader([subject], self.channels, self.datapath, batch_size=1, shuffle=False)
            for i, (data, labels) in enumerate(loader):
                transformed_data = transform_data(data)
        