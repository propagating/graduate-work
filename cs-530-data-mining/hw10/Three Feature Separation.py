import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def run_three_feature():
    data = np.loadtxt('notebooks/data/data1.csv')
    plt.figure(figsize=(6, 6))
    plt.scatter(data[:200, 0], data[:200, 1], c='blue')
    plt.scatter(data[201:400, 0], data[201:400, 1], c='red')
    plt.scatter(data[401:, 0], data[401:, 1], c='green')
    plt.grid(linestyle='--')
    plt.title('Q1-b')
    plt.show()

    blueX, blueY, blueZ = data[:200, 0], data[:200, 1], np.ones(len(data[:200, 1]))*min(data[:200, 1])
    redX, redY, redZ = data[201:400, 0], data[201:400, 1], np.ones(len(data[201:400, 1]))*min(data[201:400, 1])
    greenX, greenY, greenZ = data[401:, 0], data[401:, 1], np.ones(len(data[401:, 1]))*min(data[401:, 1])

    ax = plt.axes(projection='3d')
    ax.scatter3D(blueX, blueY, blueZ, c='blue', cmap='Blues')
    ax.scatter3D(redX, redY, redZ, c='red', cmap='Reds')
    ax.scatter3D(greenX, greenY, greenZ, c='green', cmap='Greens')
    plt.show()