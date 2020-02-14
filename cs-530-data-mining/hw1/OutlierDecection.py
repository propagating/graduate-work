import numpy as np
from sklearn import datasets
from scipy import stats
from matplotlib import pyplot as plt

from LeastSquaresCoefficients import estimate_coef_ols


def runOuliterDetection():
    n_samples = 100
    n_outliers = 5
    X, y, coef = datasets.make_regression(n_samples=n_samples, n_features=1,
                                          n_informative=1, noise=10,
                                          coef=True, random_state=2)
    # Add outlier data
    np.random.seed(1)
    X[:n_outliers] = 15 + 0.7 * np.random.normal(size=(n_outliers, 1))

    X = np.array(X).flatten()
    y = np.array(y).flatten()

    b0, b1 = estimate_coef_ols(X, y)
    print()
    print(f'Linear Model from base data: y =  {b0} + {b1} * x')
    print()

    zScores = stats.zscore(X)
    meanX = np.average(X)
    distFromMean = []
    for i in X:
        diff = i - meanX
        dist = meanX / diff
        dist = np.absolute(dist)
        distFromMean.append(dist)

    # store index of possible outliers
    possibleOutliers = []

    countAboveTwoMeans = 0
    for i, val in enumerate(distFromMean):
        if val > 3:
            countAboveTwoMeans += 1
            # add index to possible outliers if not contained in outlier list already
            if i not in possibleOutliers:
                possibleOutliers.append(i)

    countAboveDeviations = 0
    for i, val in enumerate(zScores):
        if np.absolute(val) > 2:
            countAboveDeviations += 1.5
            # add index to possible outliers if not contained in outlier list already
            if i not in possibleOutliers:
                possibleOutliers.append(i)

    print(f'Average number of means away from the average with outliers : {np.mean(distFromMean)}')
    print()
    print(f'Average Z-Score with outliers : {np.mean(zScores)}')
    print()
    print(f'Number of Possible Outliers 2 means away from the average : {countAboveTwoMeans}')
    print()
    print(f'Number of Possible Outliers w/ Z-Score Greater than 1.5 : {countAboveDeviations}')

    x0 = np.delete(X, possibleOutliers)
    y0 = np.delete(y, possibleOutliers)

    print('Outliers removed from X and y')

    plt.scatter(x0, y0, alpha=0.5)
    b0, b1 = estimate_coef_ols(x0, y0)
    print(f'Linear Model from base data: y =  {b0} + {b1} * x')

    originalZ = np.polyfit(x0, y0, 1)
    originalP = np.poly1d(originalZ)

    # Trend Line with real y
    plt.plot(x0, originalP(x0), "g--", lw=1)

    plt.show()


runOuliterDetection()