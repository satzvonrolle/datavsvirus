# necessary stuff:
# wget https://biogeo.ucdavis.edu/data/gadm3.6/shp/gadm36_DEU_shp.zip
# needs: geopandas, descartes

import pandas as pd
import geopandas as gpd

df = pd.read_csv('../data/converted/germany.csv')

germany = gpd.read_file('shapefiles/gadm36_DEU_2.shp')
germany.plot(figsize=(12, 12))



### From here on, just Lorenz' code for italy. Should just replace this by germany.
df['geometry'] = None
for region in italy['NAME_2']:
    if region in df.loc[df['Country/Region'] == 'Italy']['Province/State'].to_numpy():
        df.loc[df['Province/State'] == region].geometry = italy.loc[italy['NAME_2'] == region].geometry.array
    else:
        print(region)

# italy.loc[italy['NAME_2'] == region]
