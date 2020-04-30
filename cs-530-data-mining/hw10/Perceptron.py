import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def train_perceptron(descriptor, target, threshold=0.01, learnRate=0.1, iterations=10):
    weights = np.zeros(len(descriptor[0]))
    estimates = np.ones(len(target))
    adjustedErrors = []
    for _ in range(0, iterations):
        for i in range(0, len(descriptor)):
            f = np.dot(descriptor[i], weights)
            if f >= threshold:
                estimate = 1.
            else:
                estimate = 0.
            estimates[i] = estimate
            for j in range(0, len(weights)):
                weights[j] = weights[j] + learnRate * (target[i] - estimate) * descriptor[i][j]

        errors = np.ones(len(target))
        for i in range(0, len(target)):
            errors[i] = (target[i] - estimates[i]) ** 2
        adjustedErrors.append(0.5 * np.sum(errors))

    return weights, adjustedErrors


def test_perceptron(descriptor, weight, threshold=0.01):
    predictions = []
    for i in range(0, len(descriptor - 1)):
        f = np.dot(descriptor[i], weight)
        if f > threshold:
            prediction = 1
        else:
            prediction = 0
        predictions.append(prediction)
    return predictions


def create_descriptor(descriptor, weights):
    w0 = weights[0]
    w1 = weights[1]
    w2 = weights[2]
    outputDescriptor = []
    for i in range(0, len(descriptor - 1)):
        x2_temp = (-w0 - w1 * descriptor[i]) / w2
        outputDescriptor.append(x2_temp)
    return outputDescriptor


def run_perceptron():
    centers = [[1, 1], [2, 2]]
    X, y = make_blobs(n_samples=1000, centers=centers, cluster_std=0.2)
    plt.scatter(X[:, 0], X[:, 1])
    plt.show()

    sampleSize = 1000  # based on n_samples
    intercept = np.ones((sampleSize, 1))
    x = np.hstack((intercept, X))
    trainDescriptors, testDescriptors, trainTarget, testTarget = train_test_split(x, y, test_size=0.3)

    trainingWeights, trainingErrors = train_perceptron(trainDescriptors, trainTarget)
    epoch = np.linspace(1, len(trainingErrors), len(trainingErrors))


    plt.figure(1)
    plt.plot(epoch, trainingErrors)
    plt.xlabel('Epoch')
    plt.ylabel('Sum-of-Squared Error')
    plt.title('Perceptron Convergence')
    plt.show()
    predictedValues = test_perceptron(testDescriptors, trainingWeights)

    print(accuracy_score(testTarget, predictedValues))

    minDescriptor = np.min(testDescriptors[:, 1])
    maxDescriptor = np.max(testDescriptors[:, 1])
    firstDescriptor = np.linspace(minDescriptor, maxDescriptor, 100)
    secondDescriptor = np.asarray(create_descriptor(firstDescriptor, trainingWeights))
    plt.scatter(x[:, 1], x[:, 2], c=y)
    plt.plot(firstDescriptor, secondDescriptor)
    plt.show()