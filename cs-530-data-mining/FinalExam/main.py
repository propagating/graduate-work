import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostClassifier
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import metrics

xtrain = np.loadtxt('notebooks/data/xtrain.csv')
xtest = np.loadtxt('notebooks/data/xtest.csv')
ytrain = np.loadtxt('notebooks/data/ytrain.csv')
ytest = np.loadtxt('notebooks/data/ytest.csv')

print(xtrain.shape, xtest.shape, ytrain.shape, ytest.shape)

gamma = [0.1, 1, 10, 1000]
gammaScores = []
for g in gamma:
    clf = svm.SVC(kernel='rbf', gamma=g, C=g)
    svc_model = clf.fit(xtrain, ytrain)
    score = clf.score(xtest, ytest)
    svc_pred = svc_model.predict(xtest)
    print(score)
    print(metrics.accuracy_score(ytest, svc_pred))
    gammaScores = gammeScores.append(metrics.accuracy_score(ytest, svc_pred))

print(gammaScores)

estimators = [1, 5, 10, 20]
adaScores = []
for i in range(4):
    abc = AdaBoostClassifier(n_estimators=estimators[i],
                             learning_rate=gamma[i])
    model = abc.fit(xtrain, ytrain)
    abc_score = abc.score(xtest, ytest)
    abc_pred = model.predict(xtest)
    print(abc_score)
    print(metrics.accuracy_score(ytest, abc_pred))
    adaScores = adaScores.append(metrics.accuracy_score(ytest, abc_pred))