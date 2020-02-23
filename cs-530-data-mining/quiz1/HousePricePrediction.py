import pandas as pd
import numpy as np
from scipy.stats import stats
import statsmodels.api as sm
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


# drop Id and rename columns
def trim_train_cols(df):
    df.columns.str.contains('^id', case=False)
    trimmed = df.loc[:, ~df.columns.str.contains('^id', case=False)]

    trimmed.columns = ['SubClass', 'Zoning', 'Frontage', 'Area', 'StreetType', 'AlleyType', 'Shape', 'Contour', 'Utilities',
                       'Configuration', 'Slope', 'Neighborhood', 'FirstCondition', 'SecondCondition', 'Type', 'Style', 'TotalQuality',
                       'TotalCondition', 'YearBuilt', 'YearRemodeled', 'Roof', 'RoofMaterial', 'FirstExterior', 'SecondExterior',
                       'VeneerType', 'VeneerArea', 'ExteriorQuality', 'ExteriorCondition', 'Foundation', 'BasementQuality',
                       'BasementCondition', 'BasementExposure', 'FirstBasementFinish', 'FirstBasementSize', 'SecondBasementFinish',
                       'SecondBasementSize', 'BasementUnfinishedSize', 'TotalBasementSize', 'Heating', 'HeatingQuality', 'CentralAir',
                       'Electrical', 'FirstFloorSize', 'SecondFloorSize', 'LowQualityFinishedSize', 'AboveGradeArea',
                       'BasementFullBath', 'BasementHalfBath', 'HouseFullBath', 'HouseHalfBath', 'BedroomsAboveGrade',
                       'KitchenAboveGrade', 'KitchenQuality', 'TotalRoomsAboveGrade', 'Functional', 'Fireplace', 'FireplaceQuality',
                       'GarageType', 'GarageYear', 'GarageFinish', 'GarageCars', 'GarageArea', 'GarageQuality', 'GarageCondition',
                       'PavedDriveway', 'WoodDeckSize', 'OpenPorchSize', 'EnclosedPorch', 'AllSeasonPorch', 'ScreenPorch', 'PoolArea',
                       'PoolQuality', 'Fence', 'MiscFeature', 'MiscValue', 'MonthSold', 'YearSold', 'SaleType', 'SaleCondition',
                       'SalePrice']
    return trimmed


# convert categorical variables and populate their categorical breakdowns
def convert_categories(df):
    rank5Levels = ['Ex', 'Gd', 'TA', 'Fa', 'Po']
    rank5Exposure = ['Gd', 'Av', 'Mn', 'No', 'NA']
    rank6Levels = ['Ex', 'Gd', 'TA', 'Fa', 'Po', 'NA']
    rank7Finish = ['GLQ', 'ALQ', 'BLQ', 'Rec', 'LwQ', 'Unf', 'NA']
    functionalLevels = ['Typ', 'Min1', 'Min2', 'Mod', 'Maj1', 'Maj2', 'Sev', 'Sal']
    garageFinish = ['Fin', 'RFn', 'Unf', 'NA']
    poolLevels = ['Ex', 'Gd', 'TA', 'Fa', 'NA']
    fenceLevels = ['GdPrv', 'MnPrv', 'GdWo', 'MnWw', 'NA']
    saleLevels = ['Normal', 'Abnormal', 'AdjLand', 'Alloca', 'Family Sale', 'Partial']

    df.SubClass = df.SubClass.astype('category')
    df.Zoning = df.Zoning.astype('category')
    df.StreetType = df.StreetType.astype('category')
    df.AlleyType = df.AlleyType.astype('category')
    df.Shape = df.Shape.astype('category')
    df.Contour = df.Contour.astype('category')
    df.Utilities = df.Utilities.astype('category')
    df.Configuration = df.Configuration.astype('category')
    df.Slope = df.Slope.astype('category')
    df.Neighborhood = df.Neighborhood.astype('category')
    df.FirstCondition = df.FirstCondition.astype('category')
    df.SecondCondition = df.SecondCondition.astype('category')
    df.Type = df.Type.astype('category')
    df.Style = df.Style.astype('category')
    df.Roof = df.Roof.astype('category')
    df.RoofMaterial = df.RoofMaterial.astype('category')
    df.FirstExterior = df.FirstExterior.astype('category')
    df.SecondExterior = df.SecondExterior.astype('category')
    df.VeneerType = df.VeneerType.astype('category')
    df.Foundation = df.Foundation.astype('category')
    df.Heating = df.Heating.astype('category')
    df.CentralAir = df.CentralAir.astype('category')
    df.Electrical = df.Electrical.astype('category')
    df.GarageType = df.GarageType.astype('category')
    df.SaleType = df.SaleType.astype('category')
    df.PavedDriveway = df.PavedDriveway.astype('category')
    df.MiscFeature = df.MiscFeature.astype('category')

    df.TotalQuality = pd.Categorical(df.TotalQuality, ordered=True)
    df.TotalCondition = pd.Categorical(df.TotalCondition, ordered=True)
    df.ExteriorQuality = pd.Categorical(df.ExteriorQuality, ordered=True, categories=rank5Levels)
    df.ExteriorCondition = pd.Categorical(df.ExteriorCondition, ordered=True, categories=rank5Levels)
    df.BasementQuality = pd.Categorical(df.BasementQuality, ordered=True, categories=rank6Levels)
    df.BasementCondition = pd.Categorical(df.BasementCondition, ordered=True, categories=rank6Levels)
    df.BasementExposure = pd.Categorical(df.BasementExposure, ordered=True, categories=rank5Exposure)
    df.FirstBasementFinish = pd.Categorical(df.FirstBasementFinish, ordered=True, categories=rank7Finish)
    df.SecondBasementFinish = pd.Categorical(df.SecondBasementFinish, ordered=True, categories=rank7Finish)
    df.HeatingQuality = pd.Categorical(df.HeatingQuality, ordered=True, categories=rank5Levels)
    df.KitchenQuality = pd.Categorical(df.KitchenQuality, ordered=True, categories=rank5Levels)
    df.Functional = pd.Categorical(df.Functional, ordered=True, categories=functionalLevels)
    df.FireplaceQuality = pd.Categorical(df.FireplaceQuality, ordered=True, categories=rank6Levels)
    df.GarageFinish = pd.Categorical(df.GarageFinish, ordered=True, categories=garageFinish)
    df.GarageQuality = pd.Categorical(df.GarageQuality, ordered=True, categories=rank6Levels)
    df.GarageCondition = pd.Categorical(df.GarageCondition, ordered=True, categories=rank6Levels)
    df.PoolQuality = pd.Categorical(df.PoolQuality, ordered=True, categories=poolLevels)
    df.Fence = pd.Categorical(df.Fence, ordered=True, categories=fenceLevels)
    df.SaleCondition = pd.Categorical(df.SaleCondition, ordered=True, categories=saleLevels)
    return


# get indexes of numerical outliers
def get_numerical_outliers(df, z_thresh=3):
    constraints = df.apply(lambda x: np.abs(stats.zscore(x)) < z_thresh).all(axis=1)
    outliers = df[~constraints].index
    return outliers


# fill non-categorical NaNs with values using iterative imputing
def fill_numerical(df):
    imp = IterativeImputer(missing_values=np.nan, sample_posterior=False,
                           max_iter=10,
                           n_nearest_features=8, initial_strategy='mean')
    transformedData = pd.DataFrame(imp.fit_transform(df), columns=df.columns)
    return transformedData


# fill categorical NaNs with most prevalent category, or create a new category based on number of missing values
def fill_category(df):
    for col in df.select_dtypes('category').columns:
        dfCol = df.loc[:, col]
        counts = dfCol.value_counts()
        mostCommon = counts.index[0]
        if counts.sum() < dfCol.size / 2:
            if 'NA' in dfCol.cat.categories:
                mostCommon = 'NA'
            else:
                dfCol.cat.add_categories(['NA'], inplace=True)
                mostCommon = 'NA'
        dfCol.fillna(mostCommon, inplace=True)
    return


# default VIF calculation, adjusted for cases of over-fit and highly correlated results, set to 100 for easier number comparison
def calculate_vif(r_squared):
    if r_squared == 1:
        return 100
    vifValue = 1 / (1 - r_squared)
    return vifValue


# create the VIF datatable
def generate_vif(df):
    numerics = df.select_dtypes('number')
    numerics.columns.str.contains('^SalePrice', case=False)
    numerics = numerics.loc[:, ~numerics.columns.str.contains('^SalePrice', case=False)]

    vifFrame = pd.DataFrame(columns=['Variable', 'VIF'])

    for i in range(0, len(numerics.columns)):
        x = numerics.loc[:, numerics.columns != numerics.columns[i]]
        y = numerics.loc[:, numerics.columns == numerics.columns[i]]

        model = sm.OLS(y, sm.add_constant(x)).fit()
        vifValue = calculate_vif(model.rsquared)

        vifRecord = {'Variable': numerics.columns[i], 'VIF': vifValue}
        vifFrame = vifFrame.append(vifRecord, ignore_index=True)

    # set categorical Vif to 1 for easier processing
    categorical = df.select_dtypes('category')
    for col in categorical.columns:
        vifRecord = {'Variable': col, 'VIF': 1}
        vifFrame = vifFrame.append(vifRecord, ignore_index=True)

    return vifFrame


# pre-processing pipeline
def process_raw(train, remove_outliers):
    # convert categorical variables and populate with categories
    convert_categories(train)

    # split out numerical and categorical variables
    # fill missing categorical variables with the most prevalent, or create a new variable (NA) if more than 50% are missing values
    fill_category(train)

    # split out numerical variables and use iterative imputation to fill out NaNs
    numericalData = fill_numerical(train.select_dtypes('number'))

    for col in numericalData.columns:
        numericalCol = numericalData.loc[:, col]
        train.loc[:, col] = numericalCol

    # retrieve indices of outlier rows
    if remove_outliers:
        outlierIndices = get_numerical_outliers(numericalData, 3)
        train.drop(outlierIndices, inplace=True)
    return


# ADJUST VIF AND P-VALUES HERE TO GET DIFFERENT R-SQ and ADJ-R-SQ Values
p_threshold = 0.05
vif_threshold = 5

trainingSet = pd.read_csv('data/train.csv')
trainingData = trim_train_cols(trainingSet)
process_raw(trainingData, True)

vifScores = generate_vif(trainingData)
lowVifScores = vifScores[vifScores.VIF <= vif_threshold]

potentialDescriptors = trainingData[lowVifScores.Variable]
print(potentialDescriptors.columns)

# in order to do OLS with categorical variables, we need to split out each category into its own column
descriptors = pd.concat(
    [pd.get_dummies(potentialDescriptors.select_dtypes('category'), drop_first=True), potentialDescriptors.select_dtypes('number')], axis=1)


# first round, Adj-Rsq of .916
results = sm.OLS(trainingData['SalePrice'], sm.add_constant(descriptors, has_constant='add')).fit()
valuesToDropExist = results.pvalues > p_threshold
valuesToDropExist = valuesToDropExist[valuesToDropExist]
print(results.rsquared_adj)

# drop variables with p value less than 0.07, Adj=Rsq of .881
while len(valuesToDropExist) > 0:
    descriptorsToKeep = results.pvalues <= p_threshold
    descriptorsToKeep[0] = False
    descriptorsToKeep = descriptorsToKeep[descriptorsToKeep]
    descriptors = descriptors[descriptorsToKeep.keys()]
    results = sm.OLS(trainingData['SalePrice'], sm.add_constant(descriptors, has_constant='add')).fit()
    valuesToDropExist = results.pvalues > p_threshold
    valuesToDropExist = valuesToDropExist[valuesToDropExist]

print(results.rsquared_adj)

testingSet = pd.read_csv('data/test.csv')
testingData = trim_train_cols(trainingSet)
# don't drop outliers on test set
process_raw(testingData, False)

# in order to do OLS with categorical variables, we need to split out each category into its own column, this code should do that
predictionDescriptors = pd.concat(
    [pd.get_dummies(testingData.select_dtypes('category'), drop_first=True), testingData.select_dtypes('number')], axis=1)

predictionDescriptors.columns.str.contains('^SalePrice', case=False)
predictionDescriptors = predictionDescriptors.loc[:, ~predictionDescriptors.columns.str.contains('^SalePrice', case=False)]

predictionDescriptors = predictionDescriptors[descriptorsToKeep.keys()]
prediction = results.predict(sm.add_constant(predictionDescriptors, has_constant='add'))
print(prediction)