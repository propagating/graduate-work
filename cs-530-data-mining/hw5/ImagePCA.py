import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd


def get_principle_components(data, components):
    pca = PCA(n_components=components)
    return pca.fit_transform(data)


def generate_lin_space(x_range, y_range):
    rows = []
    for i in x_range:
        for j in y_range:
            row = [i, j]
            rows.append(row)
    np.delete(rows, 1, 1)
    np.delete(rows, 0, 1)
    return pd.DataFrame(data=rows, columns=['X-value', 'Y-value'])


def euclidean_distance(u, v):
    totalDistance = 0
    for i in range(len(u)):
        distance = np.math.sqrt((u[i] - v[i]) ** 2)
        totalDistance += distance
    return totalDistance


def get_min_distance_indexes(pcData, focusData):
    minimums = np.array([])
    for focus in focusData.values:
        distances = np.array([])
        for pc in pcData.values:
            distance = euclidean_distance(focus, pc)
            distances = np.append(distances, distance)
        min = np.argmin(distances)
        minimums = np.append(minimums, min)
    return minimums


plt.style.use('seaborn-bright')
data = pd.read_csv('notebooks/zip.train', sep=' ', index_col=0, header=None)
data = data.iloc[:, :-1]

r = data.iloc[2].values
rowData = r.reshape(16, 16)
rowImg = plt.imshow(rowData)

r = data.loc[6.0]
principleComponents = get_principle_components(r, 2)
pcData = pd.DataFrame(data=principleComponents, columns=['First', 'Second'])

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111)
x_range = np.linspace(-5,8,5)
y_range = np.linspace(-4,4,5)
focusData = generate_lin_space(x_range, y_range)
minimumIndices = get_min_distance_indexes(pcData, focusData)
print(minimumIndices)
minimumPoints = []
for i in minimumIndices:
    minimumPoints.append(pcData.values[int(i)])

print(minimumPoints)