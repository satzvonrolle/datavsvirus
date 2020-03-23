import os
import datetime as dt
import pandas as pd


print('converting italy')

basedir = 'data/raw/italy/'

regions = {
    'Abruzzo': 'ABR',
    'Basilicata': 'BAS',
    'P.A. Bolzano': 'TRE',
    'Calabria': 'CAL',
    'Campania': 'CAM',
    'Emilia Romagna': 'EMI',
    'Friuli Venezia Giulia': 'FRI',
    'Lazio': 'LAZ',
    'Liguria': 'LIG',
    'Lombardia': 'LOM',
    'Marche': 'MAR',
    'Molise': 'MOL',
    'Piemonte': 'PIE',
    'Puglia': 'PUG',
    'Sardegna': 'SAR',
    'Sicilia': 'SIC',
    'Toscana': 'TOC',
    'P.A. Trento': 'TRE',
    'Umbria': 'UMB',
    "Valle d'Aosta": 'VAL',
    'Veneto': 'VEN',
}

filename = os.listdir(basedir)[-1]
template = pd.read_csv(basedir + filename)

first = dt.date(2020, 2, 24)
mmdd = filename[6:10]
last = dt.date(2020, int(mmdd[:2]), int(mmdd[2:]))

df = pd.DataFrame({
    'Province/State': template['denominazione_provincia'] + ', ' + template['denominazione_regione'].map(regions),
    'Country/Region': 'Italy',
    'Lat': template['lat'],
    'Long': template['long'],
})

dates = [(first + dt.timedelta(days=i)) for i in range((last - first).days)]

for date in dates:
    try:
        df_tmp = pd.read_csv(basedir + f"italy_{date.strftime('%m%d')}.csv")
        cases = df_tmp['totale_casi'].to_numpy()
    except FileNotFoundError:
        cases = 0
    df[f'{date.month}/{date.day}/{date.year}'] = cases

df = df.drop(df.loc[df['Province/State'].str.contains('In fase di definizione/aggiornamento')].index)  # issue 2

df.to_csv('data/converted/italy.csv', index=False)
