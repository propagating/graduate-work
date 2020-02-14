import numpy as np
from sklearn import datasets
from matplotlib import pyplot as plt
from LeastSquaresCoefficients import estimate_coef_ols


def runLinearModel():
    n_samples = 100
    n_outliers = 5
    X, y, coef = datasets.make_regression(n_samples=n_samples, n_features=1,
                                          n_informative=1, noise=10,
                                          coef=True, random_state=2)
    # Add outlier data
    np.random.seed(1)
    X[:n_outliers] = 15 + 0.7 * np.random.normal(size=(n_outliers, 1))

    plt.scatter(X, y, alpha=0.5)
    b0, b1 = estimate_coef_ols(X, y)
    print(f'Linear Model from base data: y =  {b0} + {b1} * x')

    plt.show()

    X = np.array(X).flatten()
    y = np.array(y).flatten()

    originalZ = np.polyfit(X, y, 1)
    originalP = np.poly1d(originalZ)

    estimatedY = []

    for i in X:
        es = b0 + b1 * i
        estimatedY.append(es)

    estimatedY = np.array(estimatedY).flatten()
    estimateZ = np.polyfit(X, estimatedY, 1)
    estimateP = np.poly1d(estimateZ)

    # Trend Line with estimated Y
    plt.plot(X, estimateP(X), "r--", lw=1)

    # Trend Line with real y
    plt.plot(X, originalP(X), "g--", lw=1)

    plt.show()


runLinearModel()
