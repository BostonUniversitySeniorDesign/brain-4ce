from FBCNetwork import FBCNet
from Trainer import FBCTrainer

import argparse
import torch
import torch.nn as nn

parser = argparse.ArgumentParser(description='Argument parser example')

# Define arguments
parser.add_argument('--batch_size', type=int, default=32,
                    help='Batch size for training (default: 32)')

parser.add_argument('--datapath', type=str, default=None,
                    help='Path to data directory (default: None)')

parser.add_argument('--savepath', type=str, default='./trained_models',
                    help='Path to save directory (default: None)')

parser.add_argument('--pretrained', action='store_true', default=False,
                    help='Use a pre-trained model (default: False)')

parser.add_argument('--loadpath', type=str, default=None,
                    help='Path to pre-trained model (default: None)')

parser.add_argument('--device', type=str, default='cpu',
                    help='Device to train on (default: cpu)')

parser.add_argument('--num_epochs', type=int, default=100,
                    help='Number of epochs to train for (default: 100)')
# Parse arguments
args = parser.parse_args()

# Log cross entropy loss
class LogCrossEntropyLoss(nn.Module):
    def __init__(self):
        super(LogCrossEntropyLoss, self).__init__()

    def forward(self, input, target):
        # Compute log softmax of input
        log_probs = nn.functional.log_softmax(input, dim=1)
        # Gather log probabilities of true class labels
        loss = nn.functional.nll_loss(log_probs, target)
        return loss

channels = [2, 4, 8, 12, 15, 18, 31, 34, 42, 43, 55, 56, 58, 59, 60, 62]

# Load or create model
if(args.pretrained and args.loadpath != None):
    network = torch.load(args.loadpath)
else:
    network = FBCNet(nTime=460, nChan=len(channels), nClass=5, nBands=9, m=32, strideFactor=4, doWeightNorm=True)

# Define trainer object
trainer = FBCTrainer(network, channels=channels, batch_size=args.batch_size, fs=160, datapath=args.datapath, savepath=args.savepath)

# Define optimizer
optimizer = torch.optim.Adam(network.parameters(), lr=.001)

criterion = LogCrossEntropyLoss()

# begin training
losses, accuracies = trainer.train(device=args.device, optimizer=optimizer, criterion=criterion, nEpochs=args.num_epochs, save=True)

# test model
test_accuracy = trainer.test(device=args.device, criterion=criterion)
