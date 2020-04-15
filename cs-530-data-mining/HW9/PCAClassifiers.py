import random
import collections
import numpy as np
import pandas as pd
import pathlib as plib
import matplotlib.pyplot as plt
from path import Path as pth
from sklearn import metrics
from sklearn.decomposition import PCA
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

    def plot_decision_boundary(clf, X, y):
        cm = plt.cm.RdBu
        cm_bright = ListedColormap(['#FF0000', '#0000FF'])
        # Set up plotting mesh
        # Step size of the mesh
        h = .02
        x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
        y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))

        # Perform classification
        X_train, X_test, y_train, y_test = \
            train_test_split(X, y, test_size=.4, random_state=42)
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)
        # Plot the decision boundary. For that, we will assign a color to each

        # point in the mesh [x_min, x_max]x[y_min, y_max].
        if hasattr(clf, "decision_function"):
            Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
        else:
            Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, cmap=cm, alpha=.8)

        # Plot the training points
        plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright,
                    edgecolors='k')
        # Plot the testing points
        plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright,
                    edgecolors='k', alpha=0.6)


def run_pca(descriptors, components=2):
    standardizedDescriptors = StandardScaler().fit_transform(descriptors)
    scaledPCA = PCA(n_components=components)
    scaledDescriptors = scaledPCA.fit_transform(standardizedDescriptors)
    scaledData = pd.DataFrame(data=scaledDescriptors, columns=['PC1', 'PC2'])
    return scaledData


def run_pca_classifiers():
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
    pcaPredictionScores = pd.DataFrame({'Dataset': [], 'Classifier': [], 'Score': []})

    for dataSet in dataSets:
        p = plib.Path(dataSet)
        rawData = pd.read_csv(dataSet)
        pcaDescriptors = rawData.loc[:, :'X5']
        target = rawData['y']
        pcaDescriptors = run_pca(pcaDescriptors, 2)
        pcaTrainDescriptors, pcaTestDescriptors, pcaTrainTarget, pcaTestTarget = train_test_split(pcaDescriptors,
                                                                                                  target,
                                                                                                  test_size=0.33)
        for classifier in classifiers:
            classifierAuc = run_score_classifier(pcaTrainDescriptors, pcaTrainTarget, pcaTestDescriptors, pcaTestTarget,
                                                 classifiers[classifier])
            predictionScore = pd.DataFrame({'Dataset': [p.stem], 'Classifier': [classifier], 'Score': [classifierAuc]})
            pcaPredictionScores = pcaPredictionScores.append((predictionScore))

    def plot_pca_auc_scores(plotData, plotClassifiers, plotScores):
        barWidth = 0.1
        colors = ['#493267', '#ffad96', '#ffb554', '#c2ead8', '#87189d', '#eac2e8', '#a8b07f', '#7e5625']
        barPositionStart = np.arange(len(plotData))
        plt.xlabel('Dataset', fontweight='bold')
        plt.xticks([r + barWidth for r in range(len(plotData))], ['Set 1', 'Set 2', 'Set 3'])
        plt.yticks(np.arange(0, 1.05, step=0.05))
        plt.ylabel('AUC', fontweight='bold')

        for plotClassifier in plotClassifiers:
            classifierFilter = plotScores.Classifier == plotClassifier
            values = plotScores[classifierFilter]
            index = list(classifiers.keys()).index(plotClassifier)
            barPositions = [x + barWidth for x in barPositionStart]
            len(values)
            plt.bar(barPositions, values.Score, color=colors[index], width=barWidth, edgecolor='white',
                    label=plotClassifier)
            barPositionStart = barPositions

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=4, fancybox=True, shadow=True)
        plt.show()

    plot_pca_auc_scores(dataSets, classifiers, pcaPredictionScores)

    for dataSet in dataSets:
        p = plib.Path(dataSet)
        rawData = pd.read_csv(dataSet)
        pcaDescriptors = rawData.loc[:, :'X5']
        target = rawData['y']
        pcaDescriptors = run_pca(pcaDescriptors, 2)
        for classifier in classifiers:
            plot_decision_boundary(classifiers[classifier], pcaDescriptors.to_numpy(), target.to_numpy())
            plt.show()
