#!/usr/bin/env python
# coding: utf-8

from sklearn.decomposition import PCA
import numpy as np
import pandas as pd

# Read CSV for 2D formatted data
X = np.genfromtxt("C:\\Users\\shortallb\\Documents\\brain-4ce\\PCA\\Data\\data2D.csv", delimiter=',' )
Y = np.genfromtxt("C:\\Users\\shortallb\\Documents\\brain-4ce\\PCA\\Data\\labels2D.csv", delimiter=',' )

X = np.delete(X, 0, axis = 0)
X = np.delete(X, 0, axis = 1)
Y = np.delete(Y, 0, axis= 0)
Y = np.delete(Y, 0, axis= 1)

#Create model and fit
pca_model = PCA(n_components=16)
pca_model.fit(X)

components = np.abs(pca_model.components_)
print(components)
df = pd.DataFrame(components)
df.to_csv('./components.csv')

print(pca_model.explained_variance_ratio_)
print((pca_model.components_[1]))

# Rank features by importance
weighted_arr = np.zeros((1,64))

for i in range (0,16):
    # Scale the component values by variance ratio
    weighted_arr = np.add(weighted_arr, components[i] * pca_model.explained_variance_ratio_[i])
# Sort weighted array
sorted_ind = np.argsort(weighted_arr)
sorted_ind = np.add(sorted_ind, np.ones((1,64)))

print(sorted_ind)
pd.DataFrame(sorted_ind).to_csv('Channels_Ranked.csv')