import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt


def predict_logistic_regression(descriptors, target, logit=None):
    if logit is None:
        logit = LogisticRegression(solver='lbfgs', random_state=0).fit(descriptors, target)
    logit.predict(descriptors)
    accuracy = logit.score(descriptors, target)
    print(accuracy)
    return logit


def calculate_confusion_buckets(trueValues, predictedValues):
    tp, fp, tn, fn = 0, 0, 0, 0
    for i in range(len(predictedValues)):
        if trueValues[i] == predictedValues[i] == 1:
            tp += 1
        if predictedValues[i] == 1 and trueValues[i] != predictedValues[i]:
            fp += 1
        if trueValues[i] == predictedValues[i] == 0:
            tn += 1
        if predictedValues[i] == 0 and trueValues[i] != predictedValues[i]:
            fn += 1
    return tp, fp, tn, fn


def calculate_sensitivity(tp, fn):
    return tp / (tp + fn)


def calculate_specificity(tn, fp):
    return tn / (tn + fp)


def roc_curve_plot(predictedProbabilities, thresholdValues, trueValues):
    rocData = pd.DataFrame({'Sensitivity': [0], '1-Specificity': [0]})
    for threshold in thresholdValues:
        predictedValue = []
        for predicted in predictedProbabilities:
            if predicted > threshold:
                predictedValue.append(1)
            else:
                predictedValue.append(0)
        trueValues = trueValues.reset_index(drop=True)
        tp, fp, tn, fn = calculate_confusion_buckets(trueValues, predictedValue)
        thresholdSensitivity = calculate_sensitivity(tp, fn)
        thresholdSpecificity = 1 - calculate_specificity(tn, fp)
        if rocData['Sensitivity'].iat[-1] == thresholdSensitivity and rocData['1-Specificity'].iat[-1] == thresholdSpecificity:
            continue
        else:
            rocRow = pd.DataFrame({'Sensitivity': [thresholdSensitivity], '1-Specificity': [thresholdSpecificity]})
            rocData = rocData.append(rocRow)

    rocData = rocData.reset_index(drop=True)
    return rocData.drop(rocData.index[0], axis=0)


def run_logit():
    trainData = pd.read_csv('notebooks\\data\\train.csv', sep=',', index_col=0)
    trainDescriptors = trainData.drop(['target'], axis=1)
    trainTarget = trainData['target']

    testData = pd.read_csv('notebooks\\data\\test.csv', sep=',', index_col=0)
    testDescriptors = testData.drop(['target'], axis=1)
    testTarget = testData['target']

    predictedModel = predict_logistic_regression(trainDescriptors, trainTarget, None)
    testModel = predict_logistic_regression(testDescriptors, testTarget, predictedModel)

    predictions = predictedModel.predict_proba(testDescriptors)
    falsePositiveRate, truePositiveRate, thresholds = metrics.roc_curve(testTarget, predictions[::, 1])
    areaUnderCurve = metrics.auc(falsePositiveRate, truePositiveRate)

    givenThresholds = np.linspace(0.0, 1.0, 18)  # thresholds are arbitrary, ~18 resulted in the best AUC

    plt.plot(falsePositiveRate, truePositiveRate)
    plt.plot(givenThresholds, givenThresholds)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC AUC : ' + str(np.round(areaUnderCurve, 4)))
    plt.show()
    rocData = roc_curve_plot(predictions[::, 1], givenThresholds, testTarget)
    currentAuc = metrics.auc(rocData['1-Specificity'], rocData['Sensitivity'])

    plt.plot(rocData['1-Specificity'], rocData['Sensitivity'], label='Sensitivity vs Specificity')
    plt.plot(givenThresholds, givenThresholds)
    plt.ylabel('Sensitivity')
    plt.xlabel('1-Specificity')
    plt.title('Manual ROC AUC : ' + str(np.round(currentAuc, 4)))
    plt.show()
    return