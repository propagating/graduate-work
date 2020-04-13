import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calculate_cross_entropy(p):
    cross_entropy = 0
    for i in p:
        cross_entropy += i * np.log2(i)
    return cross_entropy * -1


def calculate_gini_index(p):
    gini_index = 0
    for i in p:
        gini_index += i * (1 - i)
    return gini_index


def calculate_misclassification_error(p):
    mc_error = 0
    for i in p:
        mc_error += i * (1 - i)
    return mc_error


def split_data_at_value(data, value):
    classification = np.array([])
    for v in data:
        if v >= value:
            classification = np.append(classification, [1])
        else:
            classification = np.append(classification, [0])
    return classification


def calculate_probability_1(data):
    total = len(data)
    ones = np.count_nonzero(data == 1)
    return ones / total


trainData = pd.read_csv('notebooks\\data\\train.csv', sep=',', index_col=0)
testData = pd.read_csv('notebooks\\data\\test.csv', sep=',', index_col=0)

giniIndex = np.array([])
crossEntropy = np.array([])
misclassification = np.array([])

for i in trainData['age']:
    split = split_data_at_value(trainData['age'], i)
    probabilities = np.array([calculate_probability_1(split)])
    cross = calculate_cross_entropy(probabilities)
    crossEntropy = np.append(crossEntropy, cross)
    gini = calculate_gini_index(probabilities)
    giniIndex = np.append(giniIndex, gini)
    misError = calculate_misclassification_error(probabilities)
    misclassification = np.append(misclassification, misError)
    print(f'split: {i}'
          f'\nprobability 1: {probabilities[0]}'
          f'\ncross entropy : {cross}'
          f'\ngini index : {gini}'
          f'\nmisclassification error : {misError}')


plt.subplot(3, 1, 1)
plt.ylim(top=.5, bottom=-.1)
plt.title('Misclassification Error')
plt.scatter(x=trainData["age"], y=misclassification)
plt.subplot(3, 1, 2)
plt.title('Gini Index')
plt.ylim(top=.5, bottom=-.1)
plt.scatter(x=trainData["age"], y=giniIndex)
plt.subplot(3, 1, 3)
plt.title('Cross Entropy')
plt.scatter(x=trainData["age"], y=crossEntropy)
plt.show()