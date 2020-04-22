import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles
from sklearn.decomposition import KernelPCA
from mpl_toolkits.mplot3d import Axes3D

def run_two_feature():
    np.random.seed(0)
    X, y = make_circles(n_samples=400, factor=.2, noise=.05)
    kpca = KernelPCA(kernel="rbf", fit_inverse_transform=True, gamma=10)
    reds = y == 0
    blues = y == 1
    X_kpca = kpca.fit_transform(X)
    X_back = kpca.inverse_transform(X_kpca)
    plt.scatter(X_back[reds, 0], X_back[reds, 1], c="red",
                s=20, edgecolor='k')
    plt.scatter(X_back[blues, 0], X_back[blues, 1], c="blue",
                s=20, edgecolor='k')
    plt.grid(linestyle='--')

    first = X[:, 0].reshape((-1, 1))
    second = X[:, 1].reshape((-1, 1))
    radius = np.sqrt(first ** 2 + second ** 2)
    theta = np.arctan2(second, first)

    colors = []
    for i in range(len(y)):
        if y[i] == 0:
            colors.append('red')
        else:
            colors.append('blue')

    fig = plt.figure()
    polarAXis = fig.add_subplot(111)
    polarAXis.scatter(theta, radius, c=colors)
    plt.show()

    third = (first ** 2 + second ** 2)
    descriptors = np.hstack((X, third))

    fig = plt.figure()
    thirdDimAxis = fig.add_subplot(111, projection='3d')
    thirdDimAxis.scatter(first, second, third, c=colors, depthshade=True)
    plt.show()