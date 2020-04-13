from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt


def predict_knn_classifier(descriptors, target, knn=None):
    if knn is None:
        knn = KNeighborsClassifier().fit(descriptors, target)
    knn.predict(descriptors)
    accuracy = knn.score(descriptors, target)
    print(accuracy)
    return knn


def euclidean_distance(u, v):
    totalDistance = 0.0
    for i in range(len(u)):
        distance = np.math.sqrt((u[i] - v[i]) ** 2)
        totalDistance += distance
    return totalDistance


def get_k_neighbours(descriptors, target, k):
    distances = list()
    for row in descriptors:
        print(row)
        dist = euclidean_distance(descriptors[row], target)
        distances.append(dist)
    distances.sort()
    neighbours = distances[:k]
    return neighbours


def predict_classification(descriptors, target, k):
    kNearestNeighbours = get_k_neighbours(descriptors, target, k)
    prediction = max(set(kNearestNeighbours), key=kNearestNeighbours.count)
    return prediction


def compute_knn_classifiers(trainDescriptors, trainTarget, k):

    return testTarget


trainData = pd.read_csv('notebooks\\data\\train.csv', sep=',', index_col=0)
trainDescriptors = trainData.drop(['target'], axis=1)
trainTarget = trainData['target']

testData = pd.read_csv('notebooks\\data\\test.csv', sep=',', index_col=0)
testDescriptors = testData.drop(['target'], axis=1)
testTarget = testData['target']

predictedModel = predict_knn_classifier(trainDescriptors, trainTarget, None)

predictions = predictedModel.predict_proba(testDescriptors)
falsePositiveRate, truePositiveRate, thresholds = metrics.roc_curve(testTarget, predictions[::, 1])
areaUnderCurve = metrics.auc(falsePositiveRate, truePositiveRate)

givenThresholds = np.linspace(0.0, 1.0, 20)
plt.plot(falsePositiveRate, truePositiveRate)
plt.plot(givenThresholds, givenThresholds)
plt.xlabel('Average False Positive Rate')
plt.ylabel('Average True Positive Rate')
plt.title('KNN ROC AUC : ' + str(np.round(areaUnderCurve, 4)))
plt.show()

pred = predict_classification(trainDescriptors, trainTarget, 5)
print(pred)
