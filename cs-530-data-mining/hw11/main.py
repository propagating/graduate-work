import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def calculate_activation(row, weight, biasWeight: float):
    activate = biasWeight
    for i in range(len(row)):
        activate += weight[i] * row[i]
    return activate


def calculate_sigmoid(activation):
    return 1 / (1 + np.e ** (-activation))


def calculate_derivative(transfer):
    return transfer * (1 - transfer)


def calculate_layer_propagation(neuronInputs, neuronWeights, neuronBias: float):
    transfer_scores = []
    for idx, row in neuronInputs.iterrows():
        activationScore = calculate_activation(row, neuronWeights, neuronBias)
        transferScore = calculate_sigmoid(activationScore)
        transfer_scores.append(transferScore)
    return transfer_scores


def calculate_error(transferScore, expectedScore):
    return (expectedScore - transferScore) * calculate_derivative(transferScore)


def calculate_back_propagation_value(neuronWeight, outputError, transferScore):
    return (neuronWeight * outputError) * calculate_derivative(transferScore)


def calculate_updated_weight(startWeight, startBias, error, learnRate: float):
    startWeight = startWeight * error * learnRate
    startBias = learnRate * startBias
    return startBias, startWeight


def train_perceptron(descriptors, target, weight, bias: float, learnRate: float, epoch: int):
    transferScores = calculate_layer_propagation(descriptors, weights, bias)
    totalError = sum([(target[i]-transferScores[i])**2 for i in range(len(target))])
    for i in weight:
        bias, weight = calculate_updated_weight(weight, bias, totalError, learnRate)
    return


X = pd.read_csv('notebooks/data/X.csv', dtype=float)
X.columns = range(X.shape[1])
y = pd.read_csv('notebooks/data/y.csv', dtype=float)
y.columns = range(y.shape[1])

trainDescriptors, testDescriptors, trainTarget, testTarget = train_test_split(X, y, test_size=0.5)

bias = 0.1
learningRate = 0.1
iterations = 1
weights = np.random.random(150, )

newDescriptors = calculate_layer_propagation(trainDescriptors, weights, bias)

print(newDescriptors)

newDescriptors = calculate_layer_propagation(trainDescriptors, weights, bias*10)

print(newDescriptors)

newDescriptors = calculate_layer_propagation(trainDescriptors, weights, bias/10)

print(newDescriptors)