import pandas as pd 
import numpy as np

cantons = ['AG', 'AI', 'AR', 'BE', 'BL', 'BS', 'FR', 'GE', 'GL', 'GR', 'JU', 'LU', 'NE', 'NW', 'OW', 'SG', 'SH', 'SZ', 'TG', 'TI', 'UR', 'VD', 'VS', 'ZG', 'ZH']
path_canton = '../../data/raw/switzerland/Canton_{}.csv'

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
long_series = pd.Series(['' for c in cantons], name='Lat')
lat_series = pd.Series(['' for c in cantons], name='Long') 
date_df = pd.DataFrame(ch, columns=dates_conv)

df = pd.concat([cantons_series, country_series, long_series, lat_series, date_df], axis=1)
df.to_csv('../../data/converted/switzerland.csv', index=False)