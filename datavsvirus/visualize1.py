# necessary stuff:
# wget https://biogeo.ucdavis.edu/data/gadm3.6/shp/gadm36_DEU_shp.zip
# needs: geopandas, descartes

import pandas as pd
import geopandas as gpd

#### BEGIN COPY PASTE FROM CONVERT
import numpy as np

import urllib.request
import json


__all__ = ['get_region_latitude_longitude']


# Use nominatim of openstreetmaps to access location data
search_url = "https://nominatim.openstreetmap.org/search.php?q={0}&format=json"


def get_region_latitude_longitude(search_string):
    """
    Get the geolocation of given region via nominatim.openstreetmaps.org .
    """
    #TODO: Implement sanity check if region is inside a given country (boundbox)

    # Whitespace and german Umlaute are not allowed
    search_string = search_string.replace(" ", "%20")
    search_string = search_string.replace("ä", "ae")
    search_string = search_string.replace("ö", "oe")
    search_string = search_string.replace("ü", "ue")
    search_string = search_string.replace("ß", "ss")

    # Get most relevant location dataset from the corresponding search_string
    with urllib.request.urlopen(search_url.format(search_string)) as url:
        data = json.loads(url.read().decode())

    # We are looking for administrative region because the case data comes from
    #  administrations. Therefore we look for region boundaries
    locations = [d for d in data \
                 if (d['class'] == 'boundary' or \
                     d['class'] == "place") \
                     and \
                    (d['type'] == 'administrative' or \
                     d['type'] == 'political' or \
                     d['type'] == 'county')]

    # Sort remaining location elements by relevance, use most relevant location
    importances = [l['importance'] for l in locations]
    highest_importance = np.argmax(importances)
    location = locations[highest_importance]

    # Return latitude and longitude
    return eval(location['lat']), eval(location['lon'])

state_mapping = {
'Baden-Württemberg': 'BW',
'Bayern': 'BY',
'Berlin': 'BE',
'Brandenburg': 'BB',
'Bremen': 'HB',
'Hamburg': 'HH',
'Hessen': 'HE',
'Mecklenburg-Vorpommern': 'MV',
'Niedersachsen': 'NI',
'Nordrhein-Westfalen': 'NW',
'Rheinland-Pfalz': 'RP',
'Saarland': 'SL',
'Sachsen': 'SN',
'Sachsen-Anhalt': 'ST',
'Schleswig-Holstein': 'SH',
'Thüringen': 'TH'}

state_ending = state_mapping.values()


def clean_up_german_province_name(province_string):
    if province_string.startswith('LK ') or province_string.startswith('SK '): 
        province_string = province_string[3:]

    for st in state_ending:
        if province_string.endswith(st):
            province_string = province_string[:-4]

    return province_string


def try_get_region_latitude_longitude(search_string):
    try:
        return get_region_latitude_longitude(search_string)
    except ValueError:
        return None, None


def get_lat_from_dict(prov_string, lookup_dict):
    return lookup_dict[prov_string][0]

    
def get_lon_from_dict(prov_string, lookup_dict):
    return lookup_dict[prov_string][1]

### END COPY PASTE FROM CONVERT

df = pd.read_csv('../data/converted/germany.csv')

germany = gpd.read_file('shapefiles/gadm36_DEU_2.shp')
germany.plot(figsize=(12, 12))

df['Province/State'] = df['Province/State'].apply(clean_up_german_province_name)

### From here on, just Lorenz' code for italy. Should just replace this by germany.
df['geometry'] = None
for region in germany['NAME_2']:
    if region in df.loc[df['Country/Region'] == 'Germany']['Province/State'].to_numpy():
        df.loc[df['Province/State'] == region].geometry = germany.loc[germany['NAME_2'] == region].geometry.array
    else:
        print(region)

# italy.loc[italy['NAME_2'] == region]


# provinces = df['Province/State].apply(clean_up_german_province_name)
