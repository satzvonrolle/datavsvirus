"""
Required packages: descartes, geopandas, pillow
"""

import geopandas
import pandas as pd
from calendar import monthrange
import matplotlib.pyplot as plt

import numpy as np

germany = geopandas.read_file("shapefiles/gadm36_DEU_2.shp")
italy = geopandas.read_file("shapefiles/gadm36_ITA_2.shp")
switzerland = geopandas.read_file("shapefiles/gadm36_CHE_2.shp")


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


all_countries2 = geopandas.GeoDataFrame( pd.concat( [germany,italy,switzerland], ignore_index=True) )

#all_countries = switzerland

italy_data = pd.read_csv("../data/converted/italy.csv")
germany_data = pd.read_csv("../data/converted/germany.csv")
switzerland_data = pd.read_csv("../data/converted/switzerland.csv")


germany_data["Province/State"] = germany_data["Province/State"].str.split(', ').str[0]
germany_data["Province/State"]  = germany_data["Province/State"].str.replace("SK ","")
germany_data["Province/State"]  = germany_data["Province/State"].str.replace("LK ","")

#germany.rename(columns={'NAME_2':'Province/State'}).concat(germany_data, axis=0, join='inner')

germany_data['geometry'] = None

maxnumber = max(germany_data["3/20/20"].max(), italy_data["3/20/20"].max() , switzerland_data["3/20/20"].max())

# logarithmic color bar
import matplotlib
from matplotlib.colors import LogNorm
log_norm = LogNorm(vmin=1, vmax=maxnumber)

current_cmap = matplotlib.cm.get_cmap()
current_cmap.set_bad(color='gray')

for month in range(1,4):
    for day in range(1, monthrange(2020, month)[1]+1):
        if  not (month==1 and day<20):
            print("Generating Month", month,"day", day)
            casedata = []
            all_countries = all_countries2.copy()

            for namefield, country, dataframe in [  ("NAME_2", "Germany", germany_data),  ("NAME_2", "Italy", italy_data),  ("NAME_1", "Switzerland", switzerland_data)]:

                for region in all_countries.loc[all_countries['NAME_0'] == country][namefield]:
                    if country=="Switzerland":
                        region = switzerdict[region]
                    #print("Search", region)
                    
                    if region in dataframe.loc[dataframe['Country/Region'] == country]['Province/State'].to_numpy():
                            key = str(month)+"/"+str(day)+"/20"
                            
                            if key in list(dataframe.columns) :
                                casedata.append(dataframe.loc[dataframe['Province/State'] == region][key].values[0])
                            else: 
                                casedata.append(0)
                            
                    else:
                        casedata.append(0)
            fig = plt.figure(num=1, figsize=(6, 8))
            fig.clf()
            all_countries.insert(2, "cases", casedata, True) 
            ax = all_countries.plot(column="cases", cmap=current_cmap, norm=log_norm, ax=fig.gca(), legend=True, vmin=0, vmax=maxnumber)
            ax.axis('off')
            ax.title.set_text('Date: ' + str(day) + '.' + str(month))
            plt.pause(.2)
            # plt.savefig("out/" + str(month).zfill(2) + "_" + str(day).zfill(2) + ".jpg")


# # ==============================================================================
# # Command to create video:
# cat *.jpg | ffmpeg -f image2pipe -r 1 -vcodec mjpeg -i - -vcodec libx264 out.mp4
