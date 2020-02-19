import pandas as pd
import numpy as np
import statsmodels.api as sm


def runMultipleRegression():
    trainingData = pd.read_csv("Data/train.csv")
    trainingData = trainingData.drop("Id", 1)

    testData = pd.read_csv("Data/test.csv")
    testData = testData.drop("Id", 1)

    trainingData.columns = ["acidity", "volatile", "citric", "sugar", "chlorides", "freeSulfur", "totalSulfur",
                            "density", "pH", "sulphates", "alcohol", "quality"]
    testData.columns = ["acidity", "volatile", "citric", "sugar", "chlorides", "freeSulfur", "totalSulfur", "density",
                        "pH", "sulphates", "alcohol"]

    # remove missing values
    trainingData.dropna()

    # separate descriptive measures from the target measure (quality)
    descriptors = trainingData.loc[:, :'alcohol']

    target = trainingData.loc[:, 'quality':]

    # store outlier index by z-score
    outliers = descriptors.apply(lambda x: np.abs(x - x.mean()) / x.std() < 3).all(axis=1)

    # remove indexes identified as outliers in target and descriptor data frames
    cleansedTarget = target[outliers]
    cleansedDescriptors = descriptors[outliers]
    print(f'Target Size w/ Outliers {target.shape}')
    print(f'Target Size w/o Outliers {cleansedTarget.shape}')

    print(f'Descriptor Size w/ Outliers {descriptors.shape}')
    print(f'Descriptor Size w/o Outliers {cleansedDescriptors.shape}')

    citricResult = sm.OLS(cleansedTarget, sm.add_constant(cleansedDescriptors['citric'])).fit()
    print(citricResult.summary())
    print(f'AIC: {citricResult.aic}')
    print(f'BIC: {citricResult.bic}')

    sulphatesResult = sm.OLS(cleansedTarget, sm.add_constant(cleansedDescriptors['sulphates'])).fit()
    print(sulphatesResult.summary())
    print(f'AIC: {sulphatesResult.aic}')
    print(f'BIC: {sulphatesResult.bic}')

    combinedResult = sm.OLS(cleansedTarget, sm.add_constant(cleansedDescriptors[['citric','sulphates']])).fit()
    print(combinedResult.summary())
    print(f'AIC: {combinedResult.aic}')
    print(f'BIC: {combinedResult.bic}')
