import numpy as np


def estimate_coef_ols(X, y):
    xCount = np.size(X)
    yCount = np.size(y)
    if xCount != yCount:
        print('X and y must have the same length in order to continue.')
        return
    # b1 = sum((xi-xbar)*(yi-ybar))/sum(xi-xbar)^2
    # b1 = sum(xi*yi +xbar*ybar -xi*ybar * yi*xbar)
    # b0 = ybar = b1*xbar
    xRes = []
    yRes = []

    for i in X:
        xRes.append(i - np.mean(X))

    for i in y:
        yRes.append(i - np.mean(y))

    sumSquare = []
    sumProd = []

    for i in range(xCount):
        sumSquare.append(xRes[i] * yRes[i])
        sumProd.append(xRes[i] * xRes[i])

    B1 = np.sum(sumSquare) / np.sum(sumProd)
    B0 = B1 * np.mean(X) - np.mean(y)
    # calculating regression coefficients(B0,B1)

    return (B0, B1)


X = [2, 4, 6, 8]
y = [1, 2, 3, 4]

print(f'Estimate Coefficients {estimate_coef_ols(X, y)}')
