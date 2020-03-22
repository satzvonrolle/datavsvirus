import datetime as dt
import pandas as pd
import numpy as np

from lookup_geolocation import get_region_latitude_longitude
from wraps_and_pd_formats import *
from functools import partial


bundesländer_mapping = {
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

df_rki = pd.read_csv('../../data/raw/germany/germany.csv')

df_rki['Meldedatum'] = pd.to_datetime(df_rki['Meldedatum'], unit='ms')

fill_empty_dates = pd.DataFrame(pd.date_range(start=dt.date(2020,1,22), end=dt.date.today()-dt.timedelta(days=1), freq='D'), columns=['Meldedatum'])
fill_empty_dates['Landkreis'] = 'LK Ahrweiler'
fill_empty_dates['Bundesland'] = 'Rheinland-Pfalz'
df_rki = df_rki.append(fill_empty_dates)
df_rki['Landkreis'] = df_rki['Landkreis'] + ', ' + df_rki['Bundesland'].map(bundesländer_mapping)

by_landkreis = pd.pivot_table(df_rki, values=['AnzahlFall'], index=['Landkreis'], columns=['Meldedatum'], aggfunc=np.sum)
by_landkreis = by_landkreis.fillna(0).cumsum(axis=1).ffill(axis=1)
by_landkreis.columns = [z[1].strftime('%m/%d/%y').lstrip("0").replace('/0', '/') for z in by_landkreis.columns]
by_landkreis = by_landkreis.astype('int32')
by_landkreis.reset_index(inplace=True)

df_build = pd.DataFrame()
df_build['Province/State'] = by_landkreis['Landkreis']
df_build['Country/Region'] = 'Germany'

# df_build['Lat'] = None
# df_build['Long'] = None

# ==============================================================================
# Add location data

# Singularize province names in the List (Do this before adding federal state)
provs_unique = list(set(df_build['Province/State'].apply(clean_up_german_province_name)))

# Write in a lookup dictionary
lookup_dict = {}
for pro in provs_unique:
    lookup_dict[pro] = try_get_region_latitude_longitude(pro)

# Some work better with 'Landkreis' in front
for pro, loc in lookup_dict.items():
    if loc == (None, None):
        lookup_dict[pro] = try_get_region_latitude_longitude('Landkreis ' + pro) 

# Some need explicit fixes
lookup_dict['StadtRegion Aachen'] = try_get_region_latitude_longitude('Aachen') 
lookup_dict['Berlin Spandau'] = try_get_region_latitude_longitude('Spandau') 
lookup_dict['Saar-Pfalz-Kreis'] = try_get_region_latitude_longitude('Saarpfalz-Kreis') 
lookup_dict['Ludwigshafen'] = (49.4704113, 8.4381568) 
lookup_dict['Lippe'] = (51.6711151, 7.7158528)

# Set map the lookup dict to be able to simply 'apply' it, 
#   Maybe there is a better way?
get_lat = partial(get_lat_from_dict, lookup_dict=lookup_dict)
get_lon = partial(get_lon_from_dict, lookup_dict=lookup_dict)

# Set Latitude and Longitude based on the 
df_build['Lat'] = df_build['Province/State'].apply(clean_up_german_province_name).apply(get_lat)
df_build['Long'] = df_build['Province/State'].apply(clean_up_german_province_name).apply(get_lon)

# End location data
# ==============================================================================

by_landkreis.drop(columns = 'Landkreis', inplace=True)
df_result = pd.concat([df_build, by_landkreis], axis=1)

df_result.to_csv('../../data/converted/germany.csv', index=False)


