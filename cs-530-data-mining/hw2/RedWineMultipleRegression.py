import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression


def preprocessing_pipeline(train):
    train.dropna()
    train.columns.str.contains('^id', case=False)
    trimmedTrain = train.loc[:, ~train.columns.str.contains('^id', case=False)]
    trimmedTrain.columns = ["acidity", "volatile", "citric", "sugar", "chlorides", "freeSulfur", "totalSulfur", "density", "pH",
                            "sulphates", "alcohol", "quality"]
    outliers = trimmedTrain.apply(lambda x: np.abs(x - x.mean()) / x.std() < 3).all(axis=1)
    processed_train = trimmedTrain[outliers]
    return processed_train


def calculate_vif(r_squared):
    vif = 1 / (1 - r_squared)

    return vif


def generate_vif_dataframe(processed_train):
    descriptors = processed_train.loc[:, :'alcohol']
    descNames = list(descriptors.columns)
    vif_dataframe = pd.DataFrame(columns=['Variable', 'VIF'])

    for i in range(0, len(descNames)):
        x = descriptors.loc[:, descriptors.columns != descNames[i]]
        y = descriptors.loc[:, descriptors.columns == descNames[i]]

        model = sm.OLS(y, sm.add_constant(x)).fit()
        vif = calculate_vif(model.rsquared)

        vif_record = {'Variable': descNames[i], 'VIF': vif}
        vif_dataframe = vif_dataframe.append(vif_record, ignore_index=True)

    return vif_dataframe


def generate_mse(original, fitted):
    sum = 0
    for i in range(0, len(original)):
        diff = original.iloc[i] - fitted.iloc[i]
        sum = sum + diff ** 2
    MSE = sum / len(original)
    return MSE


def k_fold_validation(target, descriptors, folds):
    ols = LinearRegression(fit_intercept=False)
    scores = cross_val_score(ols, descriptors, target, cv=folds)
    mean = scores.mean()
    print(f'Validation Mean Score Results {mean}')
    res = cross_val_score(ols, descriptors, target, cv=folds)
    print(f'Validation OLS Results{res}')
    predictedY = cross_val_predict(ols, descriptors, target, cv=folds)
    print(f'Validation Predicted Y Result {predictedY.mean()}')


def runRedWineRegression():

    train = pd.read_csv('data/train.csv')
    processed_train = preprocessing_pipeline(train)
    vif_dataframe = generate_vif_dataframe(processed_train)
    print(vif_dataframe)

    potentialDescriptors = vif_dataframe[vif_dataframe.VIF <= 5]
    print(potentialDescriptors.Variable)

    descriptors = processed_train[potentialDescriptors.Variable]
    results = sm.OLS(processed_train['quality'], sm.add_constant(descriptors)).fit()

    valuesToDropExist = results.pvalues > 0.07
    valuesToDropExist = valuesToDropExist[valuesToDropExist]

    while len(valuesToDropExist) > 0:
        descriptorsToKeep = results.pvalues < 0.07
        descriptorsToKeep[0] = False
        descriptorsToKeep = descriptorsToKeep[descriptorsToKeep]
        descriptors = processed_train[descriptorsToKeep.keys()]
        results = sm.OLS(processed_train['quality'], sm.add_constant(descriptors)).fit()
        valuesToDropExist = results.pvalues > 0.7
        valuesToDropExist = valuesToDropExist[valuesToDropExist]

    print(results.summary(()))

    MSE = generate_mse(processed_train['quality'], results.fittedvalues)
    print(f'Pre-Validation {MSE}')

    k_fold_validation(processed_train['quality'], descriptors, 5)

    testData = pd.read_csv("data/test.csv")
    testData = testData.drop("Id", 1)
    testData.columns = ["acidity", "volatile", "citric", "sugar", "chlorides", "freeSulfur", "totalSulfur", "density",
                        "pH",
                        "sulphates", "alcohol"]


    pred = pd.DataFrame([2.6904 - 1.181 * testData['volatile'] - .0024 * testData['totalSulfur'] + .9611 * testData['sulphates'] + .2932 *
                          testData['alcohol']])

    print(pred.shape)
    with pd.option_context('display.max_rows', 10000, 'display.max_columns', 10000):  # more options can be specified also
        print(pred.values)
        import csv
        with open('data/Prediction.csv', 'w', newline='') as csvFile:
            spamwriter = csv.writer(csvFile, delimiter=',')
            spamwriter.writerows(pred.values)
