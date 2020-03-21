import datetime as dt
import pandas as pd
import numpy as np

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
df_build['Lat'] = None
df_build['Long'] = None

by_landkreis.drop(columns = 'Landkreis', inplace=True)
df_result = pd.concat([df_build, by_landkreis], axis=1)



df_result.to_csv('../../data/converted/germany.csv', index=False)




