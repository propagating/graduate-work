from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt


def predict_linear_discriminant(descriptors, target, linearDiscriminant=None):
    if linearDiscriminant is None:
        linearDiscriminant = LinearDiscriminantAnalysis().fit(descriptors, target)
    linearDiscriminant.predict(descriptors)
    accuracy = linearDiscriminant.score(descriptors, target)
    print(accuracy)
    return linearDiscriminant


def run_lda():
    trainData = pd.read_csv('notebooks\\data\\train.csv', sep=',', index_col=0)
    trainDescriptors = trainData.drop(['target'], axis=1)
    trainTarget = trainData['target']

    testData = pd.read_csv('notebooks\\data\\test.csv', sep=',', index_col=0)
    testDescriptors = testData.drop(['target'], axis=1)
    testTarget = testData['target']

    predictedModel = predict_linear_discriminant(trainDescriptors, trainTarget, None)
    testModel = predict_linear_discriminant(testDescriptors, testTarget, predictedModel)

    predictions = predictedModel.predict_proba(testDescriptors)
    falsePositiveRate, truePositiveRate, thresholds = metrics.roc_curve(testTarget, predictions[::, 1])
    areaUnderCurve = metrics.auc(falsePositiveRate, truePositiveRate)

    givenThresholds = np.linspace(0.0, 1.0, 18)  # thresholds are arbitrary, ~18 resulted in the best AUC

    plt.plot(falsePositiveRate, truePositiveRate)
    plt.plot(givenThresholds, givenThresholds)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('LDA AUC : ' + str(np.round(areaUnderCurve, 4)))
    plt.show()

