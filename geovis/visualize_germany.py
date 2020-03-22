"""
Reuqired packages: descartes, geopandas
"""

import geopandas
import pandas as pd


germany_ = geopandas.read_file("../geodata/gadm36_DEU_2.shp")
italy = geopandas.read_file("../geodata/gadm36_ITA_2.shp")
switzerland = geopandas.read_file("../geodata/gadm36_CHE_2.shp")


switzerdict = {"Zürich": "ZH",
"Bern": "BE",
"Luzern": "LU","Lucerne": "LU", "Neuchâtel": "NE",
"Uri": "UR",
"Schwyz": "SZ",
"Obwalden": "OW",
"Nidwalden": "NW",
"Glarus": "GL",
"Zug": "ZG",
"Freiburg": "FR",
"Fribourg": "FR",
"Solothurn": "SO",
"Basel-Stadt": "BS",
"Basel-Landschaft": "BL",
"Schaffhausen": "SH",
"Appenzell Ausserrhoden": "AR",
"Appenzell Innerrhoden": "AI",
"St. Gallen": "SG","Sankt Gallen": "SG",
"Graubünden": "GR",
"Aargau": "AG",
"Thurgau": "TG",
"Tessin": "TI","Ticino": "TI",
"Waadt": "VD","Vaud": "VD",
"Wallis": "VS","Valais": "VS",
"Neuenburg": "NE",
"Genf": "GE", "Genève": "GE", "Jura": "JU"}


all_countries = geopandas.GeoDataFrame( pd.concat( [germany,italy,switzerland], ignore_index=True) )

#all_countries = switzerland

italy_data = pd.read_csv("../data/converted/italy.csv")
germany_data = pd.read_csv("../data/converted/germany.csv")
switzerland_data = pd.read_csv("../data/converted/switzerland.csv")


germany_data["Province/State"] = germany_data["Province/State"].str.split(', ').str[0]
germany_data["Province/State"]  = germany_data["Province/State"].str.replace("SK ","")
germany_data["Province/State"]  = germany_data["Province/State"].str.replace("LK ","")

#germany.rename(columns={'NAME_2':'Province/State'}).concat(germany_data, axis=0, join='inner')

germany_data['geometry'] = None
casedata = []

for namefield, country, dataframe in [  ("NAME_2", "Germany", germany_data),  ("NAME_2", "Italy", italy_data),  ("NAME_1", "Switzerland", switzerland_data)]:

    for region in all_countries.loc[all_countries['NAME_0'] == country][namefield]:
        if country=="Switzerland":
            region = switzerdict[region]
        print("Search", region)
        
        if region in dataframe.loc[dataframe['Country/Region'] == country]['Province/State'].to_numpy():
            if country=="Switzerland":
                casedata.append(dataframe.loc[dataframe['Province/State'] == region]["03/20/20"].values[0])
            else:
                casedata.append(dataframe.loc[dataframe['Province/State'] == region]["3/20/20"].values[0])
                
        else:
            casedata.append(0)



all_countries.insert(2, "cases", casedata, True) 


import matplotlib.pyplot as plt
all_countries.plot(column="cases")
plt.show()
