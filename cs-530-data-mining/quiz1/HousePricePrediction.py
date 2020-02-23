import pandas as pd
import numpy as np
from scipy.stats import stats
import statsmodels.api as sm
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


# drop Id and rename columns
def trim_test_cols(df):
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
                       'PoolQuality', 'Fence', 'MiscFeature', 'MiscValue', 'MonthSold', 'YearSold', 'SaleType', 'SaleCondition']
    return trimmed


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

    df.SubClass = pd.Categorical(df.SubClass, categories=[20, 30, 40, 45, 50, 60, 70, 75, 80, 85, 90, 120, 150, 160, 180, 190])
    df.Zoning = pd.Categorical(df.Zoning, categories=['A (agr)', 'C (all)', 'FV', 'I (all)', 'RH', 'RL', 'RM', 'RP'])
    df.StreetType = pd.Categorical(df.StreetType, categories=['Grvl', 'Pave'])
    df.AlleyType = pd.Categorical(df.AlleyType, categories=['Grvl', 'Pave', 'NA'])
    df.Shape = pd.Categorical(df.Shape, categories=['IR1', 'Reg', 'IR2', 'IR3'])
    df.Contour = pd.Categorical(df.Contour, categories=['Lvl', 'Bnk', 'Low', 'HLS'])
    df.Utilities = pd.Categorical(df.Utilities, categories=['AllPub', 'NoSewr', 'NoSeWa', 'ELO'])
    df.Configuration = pd.Categorical(df.Configuration, categories=['Inside', 'FR2', 'CulDSac', 'Corner', 'FR3'])
    df.Slope = pd.Categorical(df.Slope, categories=['Gtl', 'Mod', 'Sev'])
    df.Neighborhood = pd.Categorical(df.Neighborhood,
                                     categories=['IDOTRR', 'Somerst', 'OldTown', 'CollgCr', 'NAmes', 'Mitchel', 'MeadowV', 'Sawyer',
                                                 'BrDale', 'Edwards', 'NWAmes', 'BrkSide', 'ClearCr', 'Gilbert', 'Timber', 'SawyerW',
                                                 'Crawfor', 'SWISU', 'NridgHt', 'Veenker', 'Blueste', 'NoRidge', 'StoneBr', 'Greens',
                                                 'Blmngtn', 'NPkVill', 'GrnHill'])
    df.FirstCondition = pd.Categorical(df.FirstCondition,
                                       categories=['Norm', 'Feedr', 'Artery', 'RRAn', 'RRAe', 'PosA', 'PosN', 'RRNe', 'RRNn'])
    df.SecondCondition = pd.Categorical(df.SecondCondition, categories=['Norm', 'Feedr', 'RRNn', 'PosN', 'Artery', 'PosA'])
    df.Type = pd.Categorical(df.Type, categories=['1Fam', '2fmCon', 'Duplex', 'TwnhsE', 'Twnhs'])
    df.Style = pd.Categorical(df.Style, categories=['1Story', '2Story', '1.5Fin', '1.5Unf', '2.5Unf', 'SLvl', 'SFoyer', '2.5Fin'])
    df.Roof = pd.Categorical(df.Roof, categories=['Gable', 'Hip', 'Gambrel', 'Flat', 'Mansard', 'Shed'])
    df.RoofMaterial = pd.Categorical(df.RoofMaterial, categories=['CompShg', 'Tar&Grv', 'WdShake', 'WdShngl', 'Metal'])
    df.FirstExterior = pd.Categorical(df.FirstExterior,
                                      categories=['AsbShng', 'AsphShn', 'BrkComm', 'BrkFace', 'CBlock', 'CemntBd', 'HdBoard', 'ImStucc',
                                                  'MetalSd', 'Other', 'Plywood', 'PreCast', 'Stone', 'Stucco', 'VinylSd', 'Wd', 'WdShing'])
    df.SecondExterior = pd.Categorical(df.SecondExterior,
                                       categories=['AsbShng', 'AsphShn', 'BrkComm', 'BrkFace', 'CBlock', 'CemntBd', 'HdBoard', 'ImStucc',
                                                   'MetalSd', 'Other', 'Plywood', 'PreCast', 'Stone', 'Stucco', 'VinylSd', 'Wd', 'WdShing'])
    df.VeneerType = pd.Categorical(df.VeneerType, categories=['BrkCmn', 'BrkFace', 'CBlock', 'None', 'Stone'])
    df.Foundation = pd.Categorical(df.Foundation, categories=['BrkTil', 'CBlock', 'PConc', 'Slab', 'Stone', 'Wood'])
    df.Heating = pd.Categorical(df.Heating, categories=['Floor', 'GasA', 'GasW', 'Grav', 'OthW', 'Wall', ])
    df.CentralAir = pd.Categorical(df.CentralAir, categories=['Y', 'N'])
    df.Electrical = pd.Categorical(df.Electrical, categories=['SBrkr', 'FuseA', 'FuseF', 'FuseP', 'Mix'])
    df.GarageType = pd.Categorical(df.GarageType, categories=['2Types', 'Attchd', 'Basment', 'BuiltIn', 'CarPort', 'Detchd', 'NA'])
    df.SaleType = pd.Categorical(df.SaleType, categories=['WD', 'CWD', 'VWD', 'New', 'COD', 'Con', 'ConLw', 'ConLI', 'ConLD', 'Oth'])
    df.PavedDriveway = pd.Categorical(df.PavedDriveway, categories=['Y', 'P', 'N'])
    df.MiscFeature = pd.Categorical(df.MiscFeature, categories=['Elev', 'Gar2', 'Othr', 'Shed', 'TenC', 'NA'])

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
dummies = pd.get_dummies(potentialDescriptors.select_dtypes('category'), drop_first=True)
numbers = potentialDescriptors.select_dtypes('number')
descriptors = numbers.join(dummies)

# first round, Adj-Rsq of .916
results = sm.OLS(trainingData['SalePrice'], sm.add_constant(descriptors, has_constant='add')).fit()
print(f'Results with all variables below VIF of {vif_threshold}')
print(results.summary())

valuesToDropExist = results.pvalues > p_threshold
valuesToDropExist = valuesToDropExist[valuesToDropExist]

# drop variables with p value less than 0.07, Adj=Rsq of .881
while len(valuesToDropExist) > 0:
    descriptorsToKeep = results.pvalues <= p_threshold
    descriptorsToKeep[0] = False
    descriptorsToKeep = descriptorsToKeep[descriptorsToKeep]
    descriptors = descriptors[descriptorsToKeep.keys()]
    results = sm.OLS(trainingData['SalePrice'], sm.add_constant(descriptors, has_constant='add')).fit()
    valuesToDropExist = results.pvalues > p_threshold
    valuesToDropExist = valuesToDropExist[valuesToDropExist]

print(f'Results with all variables below VIF of {vif_threshold}, and P-value below {p_threshold}')
print(results.summary())

testingSet = pd.read_csv('data/test.csv')
testingData = trim_test_cols(testingSet)
# don't drop outliers on test set
process_raw(testingData, False)

# in order to do OLS with categorical variables, we need to split out each category into its own column, this code should do that
newDummies = pd.get_dummies(testingData.select_dtypes('category'), drop_first=True)
newNumbers = testingData.select_dtypes('number')
testDescriptors = newNumbers.join(newDummies)

testDescriptors = testDescriptors.loc[:, testDescriptors.columns.isin(descriptors.columns.values)]

prediction = results.predict(sm.add_constant(testDescriptors, has_constant='add'))
print(prediction)
