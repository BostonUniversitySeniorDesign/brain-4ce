from DataLoader import *
from Filter import FilterBank
from FBCNetwork import *



network = FBCNet(nTime=460, nChan=16, nClass=5, nBands=9, m=32, strideFactor=4, doWeightNorm=True)

def transform(data, filterbank, filter=True, convert_unit=True):
        # convert data to microvolts
        if(convert_unit):
            data = data * 1e6
        # apply filters on data
        if(filter):
            data = filterbank(data, output=True)
        return data

datapath = 'C:\\Users\\shortallb\\Documents\\brain-4ce\\PCA\\Data\\'

loader = PhysionetDataLoader([1, 2], [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], datapath, batch_size=32, shuffle=False)

filter = FilterBank([(4,8), (8, 12), (12, 16), (16,20), (20,24), (24,28), (28,32), (32,36), (36,40)], fs=160, axis=2)
for i, (data, labels) in enumerate(loader):
    # print(data[0])
    # print(transform(data[0], filter=True, convert_unit=True))
    out = network(transform(data, filter, filter=True, convert_unit=True))
    print(out)
    print(np.argmax(out.detach().numpy(), axis=1))
    print(labels)
    break
