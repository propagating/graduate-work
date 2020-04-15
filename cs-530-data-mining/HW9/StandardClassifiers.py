import random
import collections
import numpy as np
import pandas as pd
import pathlib as plib
import matplotlib.pyplot as plt
from path import Path as pth
from sklearn import metrics
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def test_train_split(data, split=0.3):
    splitSize = int(np.rint((len(data) * split)))
    splitIndices = random.sample(range(1, len(data)), splitSize)
    testData = data[data.index.isin(splitIndices)]
    trainData = data[~data.index.isin(splitIndices)]
    return testData, trainData


def run_score_classifier(trainDescriptors, trainTarget, testDescriptors, testTarget, classifierModel):
    fitModel = classifierModel.fit(trainDescriptors, trainTarget)
    predictions = fitModel.predict_proba(testDescriptors)
    falsePositiveRate, truePositiveRate, thresholds = metrics.roc_curve(testTarget, predictions[::, 1])
    classifierAuc = metrics.auc(falsePositiveRate, truePositiveRate)
    return classifierAuc


def run_standard_classifiers():
    classifiers = {
        "Nearest Neighbors": KNeighborsClassifier(3),
        "Linear SVM": SVC(kernel="linear", C=0.025, probability=True),
        "RBF SVM": SVC(gamma=2, C=1, probability=True),
        "Decision Tree": DecisionTreeClassifier(max_depth=5),
        "Random Forest": RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        "AdaBoost": AdaBoostClassifier(),
        "Naive Bayes": GaussianNB(),
        "LDA": LinearDiscriminantAnalysis()
    }

    classifiers = collections.OrderedDict(classifiers)
    absPath = pth('notebooks/data').abspath()
    dataPath = plib.Path(absPath)
    dataSets = [p for p in dataPath.iterdir() if p.is_file()]
    predictionScores = pd.DataFrame({'Dataset': [], 'Classifier': [], 'Score': []})

    for dataSet in dataSets:
        p = plib.Path(dataSet)
        rawData = pd.read_csv(dataSet)
        descriptors = rawData.loc[:, :'X5']
        target = rawData['y']
        trainDescriptors, testDescriptors, trainTarget, testTarget = train_test_split(descriptors, target,
                                                                                      test_size=0.33)
        for classifier in classifiers:
            classifierAuc = run_score_classifier(trainDescriptors, trainTarget, testDescriptors, testTarget,
                                                 classifiers[classifier])
            predictionScore = pd.DataFrame({'Dataset': [p.stem], 'Classifier': [classifier], 'Score': [classifierAuc]})
            predictionScores = predictionScores.append((predictionScore))

    barWidth = 0.1
    groupMargin = 0.4
    opacity = 0.8
    barPositionStart = np.arange(len(dataSets))
    plt.xlabel('Dataset', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(dataSets))], ['Set 1', 'Set 2', 'Set 3'])
    plt.yticks(np.arange(0, 1.05, step=0.05))
    plt.ylabel('AUC', fontweight='bold')

    colors = ['#493267', '#ffad96', '#ffb554', '#c2ead8', '#87189d', '#eac2e8', '#a8b07f', '#7e5625']

    for classifier in classifiers:
        classifierFilter = predictionScores.Classifier == classifier
        values = predictionScores[classifierFilter]
        index = list(classifiers.keys()).index(classifier)
        barPositions = [x + barWidth for x in barPositionStart]
        len(values)
        plt.bar(barPositions, values.Score, color=colors[index], width=barWidth, edgecolor='white', label=classifier)
        barPositionStart = barPositions

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=4, fancybox=True, shadow=True)
    plt.show()
