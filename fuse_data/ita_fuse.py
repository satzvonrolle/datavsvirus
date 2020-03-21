import pandas as pd
import os

names = [name for name in os.listdir('../data/') if name.startswith('ita') and name.endswith('.csv')]

def convert_to_datestring(name):
    date = name[9:13]
    month = int(date[:2])
    day = int(date[2:])
    return '%i/%i/20' % (month, day)

def extract_cases(name):
    df = pd.read_csv('../data/' + name)
    return df['totale_casi'].to_numpy()


dd = {convert_to_datestring(name): extract_cases(name) for name in names}
dd['Province/State'] = pd.read_csv('../data/' + names[0])['denominazione_provincia'].to_numpy()
dd['Country/Region'] = 'Italy'
dd['Lat'] = pd.read_csv('../data/' + names[0])['lat'].to_numpy()
dd['Long'] = pd.read_csv('../data/' + names[0])['long'].to_numpy()

df = pd.DataFrame(dd)
df.to_csv('../data/ita_fused.csv')

