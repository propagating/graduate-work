import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.metrics import silhouette_samples, silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage, fclusterdata, fcluster


def cluster_data(x, y):
    y = np.asarray(y)
    x = np.asarray(x)
    y_uniques = np.unique(y)
    return [x[y == yi] for yi in y_uniques]


def euclidean_distance(u, v):
    totalDistance = 0
    for i in range(len(u)):
        distance = np.math.sqrt((u[i] - v[i]) ** 2)
        totalDistance += distance
    return totalDistance


def update_cluster_label(centroids, cluster_labels, x):
    for i in range(len(x)):
        distance = [np.linalg.norm(x[i] - centroid) for centroid in centroids]
        label = distance.index(min(distance))
        cluster_labels.append(label)


def update_centroid(centroids, clusters):
    for i in range(len(clusters)):
        centroid = clusters[i].mean(axis=0)
        centroids[i] = centroid


def k_means(x, k=3, max_iterations=1000, tolerance=0.001):
    cluster_labels = []
    currentIterations = 0
    centroids = x[np.random.choice(x.shape[0], k, replace=False), :]

    while True:
        update_cluster_label(centroids, cluster_labels, x)
        clusters = cluster_data(x, cluster_labels)

        previousCentroids = np.array(centroids)
        update_centroid(centroids, clusters)
        currentError = np.sum((centroids - previousCentroids) / previousCentroids * 100, dtype=np.float32)
        if (currentIterations >= max_iterations) or (abs(currentError) <= tolerance):
            print(f'Iterations : {currentIterations}')
            print(f'Current Error : {currentError}')
            print(f'Current Centroids : {centroids}')
            break
        cluster_labels = []
        currentIterations += 1

    return cluster_labels


def silhouette_plot(x, y, k, ax=None):
    if ax is None:
        ax = plt.gca()

    silScores = silhouette_score(x, y)
    silValues = silhouette_samples(x, y)

    y_lower = padding = 2
    for j in range(k):
        silVal = silValues[y == j]
        silVal.sort()

        clusterSize = silVal.shape[0]
        y_upper = y_lower + clusterSize
        c_map = cm.get_cmap("Spectral")
        color = c_map(float(j) / k)
        ax.fill_betweenx(np.arange(y_lower, y_upper),
                         0,
                         silVal,
                         facecolor=color,
                         edgecolor=color,
                         alpha=0.7)

        ax.text(-0.1, y_lower + 0.5 * clusterSize, str(j + 1))
        y_lower = y_upper + padding

    ax.set_xlabel("Silhouette Value")
    ax.set_ylabel("Cluster")

    ax.axvline(x=silScores, c='r', ls='-')
    ax.annotate('Average', xytext=(silScores, y_lower * 1.025), xy=(0, 0), ha='center', alpha=0.8, c='r')
    ax.set_yticks([])
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_ylim(0, y_upper + 1)
    ax.set_xlim(-0.075, 1.0)
    return ax


def plot_data(min_c, max_c, data):
    for c in range(min_c, max_c):
        clusters = KMeans(c, random_state=10)
        clusterFit = clusters.fit_predict(data)
        fig, (ax1) = plt.subplots(1, 1, figsize=(11, 4), dpi=500)
        ax1 = silhouette_plot(data, clusterFit, c, ax=ax1)
        fig.subplots_adjust(top=0.825)
        fig.suptitle("Silhouette Analysis")
        plt.show()
        print(f'{c}, {round(silhouette_score(data, clusterFit), 2)}')


def run_silhouette():
    irisData = load_iris().data
    plot_data(2, 5, irisData)


def run_k_means():
    iris = load_iris()
    labels = np.asarray(k_means(iris.data))
    target = np.asarray(iris.target)
    comparison = pd.DataFrame({'K Means Estimate': labels, 'Iris Classification': target})
    print(comparison)
    silScores = silhouette_score(iris.data, labels)
    print(f'Average Silhouette Score {silScores}')


def run_hierarchical():
    iris = load_iris()
    links = linkage(iris.data, 'single')
    dendrogram(links, orientation='top', distance_sort='descending', show_leaf_counts=True)
    plt.title('Single Linkage')
    plt.show()
    print(fclusterdata(iris.data, t=1, method='single'))

    links = linkage(iris.data, 'complete')
    dendrogram(links, orientation='top', distance_sort='descending', show_leaf_counts=True)
    plt.title('Complete Linkage')
    plt.show()
    print(fclusterdata(iris.data, t=1, method='complete'))

    links = linkage(iris.data, 'average')
    dendrogram(links, orientation='top', distance_sort='descending', show_leaf_counts=True)
    plt.title('Average Linkage')
    plt.show()
    print(fclusterdata(iris.data, t=1, method='average'))

    links = linkage(iris.data, 'centroid')
    dendrogram(links, orientation='top', distance_sort='descending', show_leaf_counts=True)
    plt.title('Centroid Linkage')

    plt.show()
    print(fclusterdata(iris.data, t=1, method='centroid'))


    labels = fclusterdata(iris.data, method='average', criterion='maxclust', t=3)
    target = np.asarray(iris.target)
    comparison = pd.DataFrame({'K Means Estimate': labels - 1, 'Iris Classification': target})
    print(comparison)
