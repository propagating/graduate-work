import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split


def regression_tree(X_train, y_train, X_test):
    clf = tree.DecisionTreeRegressor(criterion='mse', splitter='best', max_depth=2).fit(X_train, y_train)
    score = clf.score(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(score)
    return y_pred


# make a linearly separable dataset
X, y = make_regression(n_samples=1000,
                       n_features=3)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
output = regression_tree(X_train, y_train, X_test)
