import random
import numpy as np
import pandas as pd
import pathlib as plib
import matplotlib.pyplot as plt
from path import Path as pth
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
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

def run_classifier(testData, trainData, classifier):
    w
    return


classifiers = {
    "Nearest Neighbors": KNeighborsClassifier(3),
    "Linear SVM": SVC(kernel="linear", C=0.025),
    "RBF SVM": SVC(gamma=2, C=1),
    "Decision Tree": DecisionTreeClassifier(max_depth=5),
    "Random Forest": RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    "AdaBoost": AdaBoostClassifier(),
    "Naive Bayes": GaussianNB(),
    "LDA": LinearDiscriminantAnalysis()}

absPath = pth('notebooks/data').abspath()
dataPath = plib.Path(absPath)
dataSets = [p for p in dataPath.iterdir() if p.is_file()]
print(dataSets)

for dataSet in dataSets:
    rawData = pd.read_csv(dataSet)
    testData, trainData = test_train_split(rawData, .3)
