#!/usr/bin/env python
# coding: utf-8

import xgboost as xgb
from dmatrix2np import dmatrix_to_numpy

DATA_PATH = "C:\\Users\\shortallb\\Documents\\brain-4ce\\PCA\\Data_2D.buffer"
#LABEL_PATH = 
data = xgb.DMatrix(DATA_PATH)
#data = dmatrix_to_numpy(data)

print(data.get_label)