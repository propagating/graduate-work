import numpy as np
from sklearn import linear_model as lm
from sklearn import datasets
import statsmodels.api as sm


def runStatsModel():
    n_samples = 100
    n_outliers = 5
    X, y, coef = datasets.make_regression(n_samples=n_samples, n_features=1,
                                          n_informative=1, noise=10,
                                          coef=True, random_state=2)
    # Add outlier data
    np.random.seed(1)
    X[:n_outliers] = 15 + 0.7 * np.random.normal(size=(n_outliers, 1))

    X = np.array(X)
    y = np.array(y)
    # some mistake here with the OLS Fit, but output the correct values in other models
    results = sm.OLS(X, y).fit()
    print(results.summary())

    outTest = results.outlier_test()
    outliers = ((X[i], y[i])
                for i, t in enumerate(outTest)
                if t[2] < 0.5)
    print('Outliers: ', list(outliers))

    reg = lm.LinearRegression().fit(X, y)
    reg.score(X, y)
    print(reg.coef_)
    print(reg.intercept_)
    print(reg.score)


runStatsModel()
