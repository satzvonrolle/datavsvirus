"""
Reuqired packages: descartes, geopandas
"""

import geopandas
import pandas as pd


germany = geopandas.read_file("../geodata/gadm36_DEU_2.shp")
italy = geopandas.read_file("../geodata/gadm36_ITA_2.shp")

all_countries = geopandas.GeoDataFrame( pd.concat( [germany,italy], ignore_index=True) )



italy_data = pd.read_csv("../data/converted/italy.csv")
germany_data = pd.read_csv("../data/converted/germany.csv")

germany_data["Province/State"] = germany_data["Province/State"].str.split(', ').str[0]
germany_data["Province/State"]  = germany_data["Province/State"].str.replace("SK ","")
germany_data["Province/State"]  = germany_data["Province/State"].str.replace("LK ","")

#germany.rename(columns={'NAME_2':'Province/State'}).concat(germany_data, axis=0, join='inner')

germany_data['geometry'] = None
casedata = []

for region in all_countries['NAME_2']:
    if region in germany_data.loc[germany_data['Country/Region'] == 'Germany']['Province/State'].to_numpy():
        casedata.append(germany_data.loc[germany_data['Province/State'] == region]["3/20/20"].values[0])
    elif region in italy_data.loc[germany_data['Country/Region'] == 'Italy']['Province/State'].to_numpy():
        casedata.append(germany_data.loc[germany_data['Province/State'] == region]["3/20/20"].values[0])
    else:
        casedata.append(0)


all_countries.insert(2, "cases", casedata, True) 


import matplotlib.pyplot as plt
all_countries.plot(column='cases')
plt.show()
