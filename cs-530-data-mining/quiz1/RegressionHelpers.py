from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import pandas as pd


def calculate_vif(r_squared):
    vif = 1 / (1 - r_squared)

    return vif


def generate_mse(original, fitted):
    sum = 0
    for i in range(0, len(original)):
        diff = original.iloc[i] - fitted.iloc[i]
        sum = sum + diff ** 2
    MSE = sum / len(original)
    return MSE


def generate_vif_data(processed_train):
    descriptors = processed_train.loc[:, :'alcohol']
    descNames = list(descriptors.columns)
    vif_data = pd.DataFrame(columns=['Variable', 'VIF'])

    for i in range(0, len(descNames)):
        x = descriptors.loc[:, descriptors.columns != descNames[i]]
        y = descriptors.loc[:, descriptors.columns == descNames[i]]

        model = sm.OLS(y, sm.add_constant(x)).fit()
        vif = calculate_vif(model.rsquared)

        vif_record = {'Variable': descNames[i], 'VIF': vif}
        vif_data = vif_data.append(vif_record, ignore_index=True)

    return vif_data


def k_fold_validation(target, descriptors, folds):
    ols = LinearRegression(fit_intercept=False)
    scores = cross_val_score(ols, descriptors, target, cv=folds)
    mean = scores.mean()
    print(f'Validation Mean Score Results {mean}')
    res = cross_val_score(ols, descriptors, target, cv=folds)
    print(f'Validation OLS Results{res}')
    predictedY = cross_val_predict(ols, descriptors, target, cv=folds)
    print(f'Validation Predicted Y Result {predictedY.mean()}')
