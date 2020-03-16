from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn import datasets
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import random


X, y = datasets.make_classification(n_samples=2000, n_features=20,
                                    n_informative=3)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

def predict_logistic_regression(descriptors, target, logit=None):
    if logit is None:
        logit = LogisticRegression(solver='lbfgs', random_state=0, max_iter=10000).fit(descriptors, target)
    logit.predict(descriptors)
    return logit

def score_logit(descriptors, target, logit):
    predictions = logit.predict_proba(descriptors)
    falsePositiveRate, truePositiveRate, thresholds = metrics.roc_curve(target, predictions[::, 1])
    areaUnderCurve = metrics.auc(falsePositiveRate, truePositiveRate)
    return areaUnderCurve

def run_logit_random():
    print('Train Data')
    predictedModel = predict_logistic_regression(X_train, y_train, None)
    print(predictedModel.score(X_train, y_train))
    print('Test Data')
    testModel = predict_logistic_regression(X_test, y_test, predictedModel)
    print(testModel.score(X_test, y_test))

    areaUnderCurve = score_logit(X_test, y_test, predictedModel)

    print('AUC')
    print(areaUnderCurve)

    aucHundred = []
    aucThreeHundred = []
    aucThousand = []

    for i in range(1000):
        hundredIndexes = random.sample(range(len(X_train)), 100)
        threeHundredIndexes = random.sample(range(len(X_train)), 300)
        thousandIndexes = random.sample(range(len(X_train)), 1000)

        hundredPredicted = predict_logistic_regression(X_train[hundredIndexes], y_train[hundredIndexes], None)
        threeHundredPredicted = predict_logistic_regression(X_train[threeHundredIndexes], y_train[threeHundredIndexes], None)
        thousandPredicted = predict_logistic_regression(X_train[thousandIndexes], y_train[thousandIndexes], None)

        aucHundred.append(score_logit(X_test, y_test, hundredPredicted))
        aucThreeHundred.append(score_logit(X_test, y_test, threeHundredPredicted))
        aucThousand.append(score_logit(X_test, y_test, thousandPredicted))

    bins = np.linspace(min(aucHundred), max(aucThousand), 100)
    plt.axvline(areaUnderCurve, color='black', label='Full Sample AUC', linestyle='-')
    plt.hist(aucHundred, bins, alpha=0.8, label='100 Sample')
    plt.hist(aucThreeHundred, bins, alpha=0.8, label='300 Sample')
    plt.hist(aucThousand, bins, alpha=0.8, label='1000 Sample')
    plt.legend(loc='best')
    plt.show()
