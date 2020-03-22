"""
Reuqired packages: descartes, geopandas
"""

import geopandas
import pandas as pd


germany = geopandas.read_file("../geodata/gadm36_DEU_2.shp")

germany_data = pd.read_csv("../data/converted/germany.csv")
germany_data["Province/State"] = germany_data["Province/State"].str.split(', ').str[0]
germany_data["Province/State"]  = germany_data["Province/State"].str.replace("SK ","")
germany_data["Province/State"]  = germany_data["Province/State"].str.replace("LK ","")

#germany.rename(columns={'NAME_2':'Province/State'}).concat(germany_data, axis=0, join='inner')


import matplotlib.pyplot as plt
germany.plot()
plt.show()
