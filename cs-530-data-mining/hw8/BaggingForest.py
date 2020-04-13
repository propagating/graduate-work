import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score


def fit_bag_est(desc, target, estimators=10):
    bag = BaggingClassifier(n_estimators=estimators, oob_score=True)
    bag.fit(desc, target)
    score = bag.oob_score_
    print(score)
    return bag


def fit_forest_est(desc, target, estimators=10):
    forrest = RandomForestClassifier(n_estimators=estimators, oob_score=True)
    forrest.fit(desc, target)
    score = forrest.oob_score_
    print(score)
    return forrest


def calc_roc(trainTarget, testTarget, predictor):
    confusion_matrix = pd.crosstab(testTarget, predictor)
    metrics.accuracy_score(testTarget, predictor)
    predict_probabilities = predictor.predict_proba(trainTarget)
    fpr, tpr, thr = metrics.roc_curve(testTarget, predict_probabilities[:, 1])
    return fpr, tpr, thr


trainData = pd.read_csv('notebooks\\data\\train.csv', sep=',', index_col=0)
testData = pd.read_csv('notebooks\\data\\test.csv', sep=',', index_col=0)

trainDescriptors = trainData.drop(columns=['target'], axis=1)
trainTarget = trainData['target']

testDescriptors = testData.drop(columns=['target'], axis=1)
testTarget = testData['target']

bagEst = fit_bag_est(trainDescriptors, trainTarget, 100)
bagPredictor = bagEst.predict(testDescriptors)
print(bagPredictor)

forrestEst = fit_bag_est(trainDescriptors, trainTarget, 100)
forrestPredictor = forrestEst.predict(testDescriptors)
print(forrestPredictor)


descriptors = len(trainDescriptors.columns)
maxSplit = 5

minEstimators = 1
maxEstimators = descriptors * maxSplit

bagError = np.array([])
forrestError = np.array([])

for i in range(minEstimators, maxEstimators):
    bagEst = fit_bag_est(trainDescriptors, trainTarget, i)
    bagPredictor = bagEst.predict(testDescriptors)
    bagError = np.append(bagError, bagEst.oob_score_)

    forrestEst = fit_bag_est(trainDescriptors, trainTarget, i)
    forrestPredictor = forrestEst.predict(testDescriptors)
    forrestError = np.append(forrestError, forrestEst.oob_score_)

x = range(minEstimators, maxEstimators)
plt.plot(x, bagError)
plt.show()

x = range(minEstimators, maxEstimators)
plt.plot(x, forrestError)
plt.show()

bagMinIndex = np.where(bagError == np.amin(bagError))
numPredictors = x[bagMinIndex]
bagEst = fit_bag_est(trainDescriptors, trainTarget, numPredictors)
bagPredictor = bagEst.predict(testDescriptors)
fpr, tpr, thr = calc_roc(trainTarget, testTarget, bagEst)
plt.plot(fpr, tpr, 'navy', lw=1)

forrestMinIndex = np.where(forrestError == np.amin(forrestError))
numPredictors = x[forrestMinIndex]
forrestEst = fit_bag_est(trainDescriptors, trainTarget, numPredictors)
forrestPredictor = forrestEst.predict(testDescriptors)
fpr, tpr, thr = calc_roc(trainTarget, testTarget, forrestEst)
plt.plot(fpr, tpr, 'navy', lw=1)
