import pandas as pd
import os

basedir = '../../data/raw/italy/'

names = [name for name in os.listdir(basedir) if name.endswith('.csv')]
tmp = pd.read_csv(basedir + names[0])


def convert_to_datestring(name):
    date = name[6:10]
    month = int(date[:2])
    day = int(date[2:])
    return '%i/%i/20' % (month, day)


def extract_cases(name):
    df = pd.read_csv(basedir + name)
    return df['totale_casi'].to_numpy()


dd = {convert_to_datestring(name): extract_cases(name) for name in names}
dd['Province/State'] = tmp['denominazione_provincia']
dd['Country/Region'] = 'Italy'
dd['Lat'] = tmp['lat']
dd['Long'] = tmp['long']

df = pd.DataFrame(dd)
df = df.drop(df.loc[df['Province/State'] == 'In fase di definizione/aggiornamento'].index)  # issue 2

for column in pd.read_csv('../../data/raw/reference.csv').columns:
    if column not in df:
        df[column] = 0

df.to_csv('../../data/converted/italy.csv', index=False)
