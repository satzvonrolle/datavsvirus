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

ita_df = pd.DataFrame(dd)

jhu_df = pd.read_csv('../data/jhu_data_Confirmed.csv')

series = jhu_df.loc[jhu_df['Country/Region'] == 'Italy']

for column in jhu_df.columns:
    if column not in ita_df:
        ita_df[column] = 0

df = pd.concat([jhu_df, ita_df], ignore_index=True)
df = df.drop(df.loc[(df['Country/Region'] == 'Italy') & (df['Province/State'].isnull())].index)

df.to_csv('../data/jhu_data_Confirmed_with_italy.csv', index=False)
