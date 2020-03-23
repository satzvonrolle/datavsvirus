import os
import numpy as np

import pandas as pd 
import json

from functools import partial

from datavsvirus.utils.lookup_geolocation import get_region_latitude_longitude
from datavsvirus.utils.wraps_and_pd_formats import \
    try_get_region_latitude_longitude, \
    clean_up_german_province_name, switzerland_abbrev_mapping, \
    get_lon_from_dict, get_lat_from_dict


print('converting switzerland')

cantons = ['AG', 'AI', 'AR', 'BE', 'BL', 'BS', 'FR', 'GE', 'GL', 'GR', 'JU', 'LU', 'NE', 'NW', 'OW', 'SG', 'SH', 'SZ', 'TG', 'TI', 'UR', 'VD', 'VS', 'ZG', 'ZH']
path_canton = 'data/raw/switzerland/Canton_{}.csv'

feb = ['2020-02-{:02}'.format(d) for d in range(25, 30)]
mar = ['2020-03-{:02}'.format(d) for d in range(1, 23)]  # Todo: more general, until today
dates = feb + mar

ch = np.zeros((len(cantons), len(dates)), dtype=int)
for c, canton in enumerate(cantons):
    prev_value = 0
    canton_data = pd.read_csv(path_canton.format(canton))
    canton_dates = canton_data['date']
    for d, date in enumerate(dates):
        value = canton_data.loc[(canton_data['date'] == date)]['ncumul_conf'].values
        if len(value) and not np.isnan(value[0]):  # found valid entry for that date
            prev_value = value[0]
            ch[c, d] = value[0]
        else:
            ch[c, d] = prev_value  # no valid entry --> write previous one

dates_conv = ['{}/{}/{}'.format(int(d.split('-')[1]), int(d.split('-')[2]), d.split('-')[0][2:]) for d in dates]
cantons_series = pd.Series(cantons, name='Province/State')
country_series = pd.Series(['Switzerland' for c in cantons], name='Country/Region')

# ==============================================================================
# Load geolocation data for switzerland

# Write in a lookup dictionary
path_locations_sw = 'data/raw/switzerland/locations_switzerland.json'

if os.path.exists(path_locations_sw):
    # Read data from file:
    lookup_dict = json.load(open(path_locations_sw))

else:
    lookup_dict = {}

    # Use geolookup with nominatim.openstreetmaps
    for pro in cantons_series.map(switzerland_abbrev_mapping):
        lookup_dict[pro] = try_get_region_latitude_longitude(pro)

    # Format to four decimal digits like in Johns Hopkins Uni format
    for pro, loc in lookup_dict.items():
        lookup_dict[pro] = (np.around(loc[0], 4), np.around(loc[1], 4))

    # Serialize data into file:
    json.dump(lookup_dict, open(path_locations_sw, 'w'))

get_lat = partial(get_lat_from_dict, lookup_dict=lookup_dict)
get_lon = partial(get_lon_from_dict, lookup_dict=lookup_dict)

long_series = pd.Series(cantons_series.map(switzerland_abbrev_mapping).apply(get_lat), name='Lat')
lat_series = pd.Series(cantons_series.map(switzerland_abbrev_mapping).apply(get_lon), name='Long')

date_df = pd.DataFrame(ch, columns=dates_conv)

df = pd.concat([cantons_series, country_series, long_series, lat_series, date_df], axis=1)
df.to_csv('data/converted/switzerland.csv', index=False)
