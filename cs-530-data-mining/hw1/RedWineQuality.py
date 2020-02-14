import pandas as pd
import statsmodels.formula.api as sm
import numpy as np
from matplotlib import pyplot as plt


def runRedWine():
    trainingData = pd.read_csv("Data/train.csv")
    testData = pd.read_csv("Data/test.csv")
    trainingData = trainingData.drop("Id", 1)
    testData = testData.drop("Id", 1)

    trainingData.columns = ["acidity", "volatile", "citric", "sugar", "chlorides", "freeSulfur", "totalSulfur",
                            "density",
                            "pH", "sulphates", "alcohol", "quality"]
    testData.columns = ["acidity", "volatile", "citric", "sugar", "chlorides", "freeSulfur", "totalSulfur", "density",
                        "pH",
                        "sulphates", "alcohol"]

    qualityOutliers = trainingData[trainingData['quality'] > 8].index

    trainingData.drop(qualityOutliers, inplace=True)
    regression = sm.ols(formula="quality ~ volatile+ chlorides+ totalSulfur+ pH+sulphates+ alcohol",
                        data=trainingData).fit()

    print(regression.summary())
    simpleRegression = sm.ols(formula="quality~volatile", data=trainingData).fit()
    print(simpleRegression.summary())

    plt.scatter(trainingData['volatile'], trainingData['quality'])

    plt.xlabel('Volatile Acidity Content')
    plt.ylabel('Quality Rating')

    label = 'Adjusted R-Square:', simpleRegression.rsquared
    plt.title(label)

    trainingData.dropna(inplace=True)

    trendX = trainingData['volatile']
    trendY = trainingData['quality']

    trendZ = np.polyfit(trendX, trendY, 1)
    trendP = np.poly1d(trendZ)

    plt.plot(trendX, trendP(trendX), "r--")

    plt.show()

    print(trendP(testData['volatile']))


runRedWine()
