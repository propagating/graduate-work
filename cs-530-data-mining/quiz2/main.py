import numpy as np
from numpy import array
from numpy import mean
from numpy import cov
from numpy.linalg import eig
from scipy.linalg import svd


def caculate_percentage_of_variance(eigen_values, components):
    totalVar = 0
    for i in eigen_values:
        totalVar += eigen_values[i]

    list_of_percentages = []
    for i in eigen_values:
        list_of_percentages.append(i/totalVar)
    return list_of_percentages


def pca(X, components=2):
    colMeans = mean(X.T, axis=1)
    print(colMeans)
    colCenter = X - colMeans
    print(colCenter)
    xVariance = cov(colCenter.T)
    print((xVariance))
    values, vectors = eig(xVariance)
    pcs = []

    list_of_percentages = caculate_percentage_of_variance(pcs, components)

    return pcs, list_of_percentages


X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])

pca(X, 2)
