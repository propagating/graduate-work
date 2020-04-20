import numpy as np
import pandas as pd
import plotly.express as px
import plotly.offline as py
from opencage.geocoder import OpenCageGeocode


def update_row_data(data):
    key = '10ff0ab8fe6a481fad3b1618a6b62ffc'
    geoCoder = OpenCageGeocode(key)

    for i, row in data.iterrows():
        print(i)
        country = row['Country or region']
        forward = geoCoder.geocode(country)
        try:  # Some countries don't have ISO3 codes and need to use ISO2 codes instead
            data.at[i, 'Country Code'] = forward[0]['components']['ISO_3166-1_alpha-3']
        except KeyError:
            data.at[i, 'Country Code'] = forward[0]['components']['ISO_3166-1_alpha-2']
        data.at[i, 'latitude'] = forward[0]['geometry']['lat']
        data.at[i, 'longitude'] = forward[0]['geometry']['lng']

    data.to_csv('notebooks\\data\\2019mod.csv', index=False)
    return data


data = pd.read_csv(r"notebooks\\data\\2019mod.csv")
#if data['latitude'].values[0] == 1.01:
#    data = update_row_data(data)

dataSerial = data[['Country or region', 'Country Code', 'Score']]

plotData = [dict(type='choropleth',
                 locations=data['Country Code'],
                 z=data['Score'],
                 text=data['Country or region'],
                 colorscale=[[0, "rgb(244, 120, 109)"], [0.25, "rgb(255, 162, 105)"],
                             [0.5, "rgb(255, 255, 255)"], [0.75, "rgb(171, 213, 236)"],
                             [1, "rgb(150, 187, 216)"]],
                 autocolorscale=False,
                 reversescale=True,
                 marker=dict(line=dict(color='rgb(0,0,0)', width=0.5)),
                 colorbar=dict(autotick=False, title='Happiness', thickness=15, len=0.6,
                               tickfont=dict(size=14), titlefont=dict(size=14)), )]

plotLayout = dict(title='Happiness by Country',
                  font=dict(size=18),
                  geo=dict(showframe=False, showcoastlines=False,
                           projection=dict(type='Mercator')))

fig = dict(data=plotData, layout=plotLayout)
py.iplot(fig, validate=False, filename='worldHappiness')

bubbleFig = px.scatter_geo(data,
                           title='GDP effect on Happiness',
                           locations='Country Code', color='GDP per capita',
                           hover_name='Country or region',
                           size='Score',
                           projection='natural earth',
                           color_continuous_scale=px.colors.diverging.BrBG,
                           color_continuous_midpoint=np.mean(data['GDP per capita']),
                           opacity=1)

# bubbleFig.show()