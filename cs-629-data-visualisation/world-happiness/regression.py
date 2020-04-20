import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
import plotly.figure_factory as ff


def calculate_vif(r_squared):
    ## Your code goes here
    vif = 1 / (1 - r_squared)
    return vif


def generate_vif_dataframe(processed_train):
    ## Your code goes here
    vif_scores = []
    var = []

    new_data = processed_train.drop(['Country or region', 'Score'], axis=1)

    for i in new_data.columns:
        var = [i]
        x = new_data.drop(i, axis=1).values
        y = new_data[i].values

        # calculate regression
        s = sm.add_constant(x)
        results = sm.OLS(y, s).fit()
        r2 = results.rsquared

        vif = round(calculate_vif(r2), 3)
        var.append(vif)
        vif_scores.append(var)

        vif_dataframe = pd.DataFrame(vif_scores, columns=['Variable', 'VIF'])

    return vif_dataframe


data = pd.read_csv("notebooks/data/2019.csv", index_col=0)
score = data['Score']
generate_vif_dataframe(data)
x = data.drop(['Score', 'Country or region'], axis=1)
y = data['Score']

col = x.columns
corr = []
for i in range(len(col)):
    r = round(np.corrcoef(x.iloc[:, i], y)[0, 1], 3)
    corr.append(r)

plt.scatter(x.iloc[:, 0], y, c=y, label='R Score: ' + str(corr[0]), cmap='coolwarm')
plt.xlabel(col[0], fontsize=16)
plt.ylabel('Happiness Score', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.colorbar(label='Happiness')
plt.legend(fontsize=14)
plt.show()

plt.scatter(x.iloc[:, 1], y, c=y, label='R Score: ' + str(corr[1]), cmap='coolwarm')
plt.xlabel(col[1], fontsize=16)
plt.ylabel('Happiness Score', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.colorbar(label='Happiness')
plt.legend(fontsize=14)
plt.show()
plt
# plt.savefig('Social Support.png')

plt.scatter(x.iloc[:, 2], y, c=y, label='R Score: ' + str(corr[2]), cmap='coolwarm')
plt.xlabel(col[2], fontsize=16)
plt.ylabel('Happiness Score', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.colorbar(label='Happiness')
plt.legend(fontsize=14)
plt.show()
# plt.savefig('Life Expectancy.png')

plt.scatter(x.iloc[:, 3], y, c=y, label='R Score: ' + str(corr[3]), cmap='coolwarm')
plt.xlabel(col[3], fontsize=16)
plt.ylabel('Happiness Score', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.colorbar(label='Happiness')
plt.legend(fontsize=14)
plt.show()
# plt.savefig('Freedom.png')


plt.scatter(x.iloc[:, 4], y, c=y, label='R Score: ' + str(corr[4]), cmap='coolwarm')
plt.xlabel(col[4], fontsize=16)
plt.ylabel('Happiness Score', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.colorbar(label='Happiness')
plt.legend(fontsize=14)
plt.show()
# plt.savefig('Generosity.png')

plt.scatter(x.iloc[:, 5], y, c=y, label='R Score: ' + str(corr[5]), cmap='coolwarm')
plt.xlabel(col[5], fontsize=16)
plt.ylabel('Happiness Score', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.colorbar(label='Happiness')
plt.legend(fontsize=14)
plt.show()
# plt.savefig('Corruption.png')
