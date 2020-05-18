import numpy as np


xtrain = np.loadtxt('notebooks/data/xtrain.csv')
xtest = np.loadtxt('notebooks/data/xtest.csv')
ytrain = np.loadtxt('notebooks/data/ytrain.csv')
ytest = np.loadtxt('notebooks/data/ytest.csv')

print(xtrain.shape, xtest.shape, ytrain.shape, ytest.shape )
xtrain1 = xtrain.reshape((xtrain.shape[0], 28,28))
print(xtrain1.shape)
