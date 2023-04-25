import torch
import torch.nn as nn


# Inherits Conv2d base class and adds weight normalization and max norm constraint
class Conv2dWithConstraint(nn.Conv2d):
    def __init__(self, *args, doWeightNorm = True, max_norm=1, **kwargs):
        self.max_norm = max_norm
        self.doWeightNorm = doWeightNorm
        super(Conv2dWithConstraint, self).__init__(*args, **kwargs)

    def forward(self, x):
        if self.doWeightNorm:
            # renorm weights to satisfy max_norm constraint 
            self.weight.data = torch.renorm(
                self.weight.data, p=2, dim=0, maxnorm=self.max_norm
            )
        return super(Conv2dWithConstraint, self).forward(x)


# Inherits Linear base class and adds weight normalization and max norm constraint
class LinearWithConstraint(nn.Linear):
    def __init__(self, *args, doWeightNorm = True, max_norm=1, **kwargs):
        self.max_norm = max_norm
        self.doWeightNorm = doWeightNorm
        super(LinearWithConstraint, self).__init__(*args, **kwargs)

    def forward(self, x):
        if self.doWeightNorm:
            # renorm weights to satisfy max_norm constraint 
            self.weight.data = torch.renorm(
                self.weight.data, p=2, dim=0, maxnorm=self.max_norm
            )
        return super(LinearWithConstraint, self).forward(x)


class swish(nn.Module):
    #Implementation of the swish activation function
    def __init__(self):
        super(swish, self).__init__()
    
    def forward(self, x):
        return x * torch.sigmoid(x)


class LogVarLayer(nn.Module):
    #Calculates the log variance of the data along the given dimension
    def __init__(self, dim):
        super(LogVarLayer, self).__init__()
        self.dim = dim

    def forward(self, x):
        return torch.log(torch.clamp(x.var(dim = self.dim, keepdim= True), 1e-6, 1e6))


class FBCNet(nn.Module):
    #Implementation of the FBCNet architecture using a logvar temporal layer
    def __init__(self, nTime, nChan = 16, nClass = 5, nBands = 9, m = 32, strideFactor= 4, doWeightNorm = True):
        super(FBCNet, self).__init__()
    
        # number of frequency bands
        self.nBands = nBands
        # number of spatial filters per band
        self.m = m
        self.strideFactor = strideFactor

        # spatial convolution block (SCB)
        self.scb = nn.Sequential(
            Conv2dWithConstraint(nBands, m*nBands, (nChan, 1), groups=nBands, max_norm=2, doWeightNorm=doWeightNorm, padding=0),
            nn.BatchNorm2d(m*nBands),
            swish()
        )

        # Original implementation allows for different kinds of temporal layers - this implementation only uses log variance 
        self.temporalLayer = LogVarLayer(dim=3)

        # last layer of the network
        # sequential layer with a constrained fully connected layer followed by a softmax layer
        self.lastLayer = nn.Sequential(
            LinearWithConstraint(m*nBands*strideFactor, nClass, max_norm=2, doWeightNorm=doWeightNorm),
            nn.LogSoftmax(dim=1)
        )

    def forward(self,x):
        # input x is of shape (batch_size, nChan, nTime, nBands)
        # reshape to size (batch_size, nBands, nChan, nTime)
        x = x.permute(0,3,1,2)
        # apply spatial convolution block
        x = self.scb(x)
        # reduce temporal dimension by factor of strideFactor
        x = x.reshape([*x.shape[0:2], self.strideFactor, int(x.shape[3]/self.strideFactor)])

        # apply temporal layer
        x = self.temporalLayer(x)
        x = torch.flatten(x, start_dim= 1)

        # apply last layer
        x = self.lastLayer(x)
        return x