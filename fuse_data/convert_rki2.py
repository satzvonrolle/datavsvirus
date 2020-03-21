import datetime as dt
import pandas as pd
import numpy as np


df_rki = pd.read_csv('../data/rki_daten.csv')

df_rki['Meldedatum'] = pd.to_datetime(df_rki['Meldedatum'], unit='ms')

fill_empty_dates = pd.DataFrame(pd.date_range(start=dt.date(2020,1,22), end=dt.date.today(), freq='D'), columns=['Meldedatum'])
fill_empty_dates['Landkreis'] = 'LK Ahrweiler'
df_rki = df_rki.append(fill_empty_dates)

by_landkreis = pd.pivot_table(df_rki, values=['AnzahlFall'], index=['Landkreis'], columns=['Meldedatum'], aggfunc=np.sum)
by_landkreis = by_landkreis.fillna(0).cumsum(axis=1).ffill(axis=1)
by_landkreis.columns = [z[1].strftime('%d/%m/%y') for z in by_landkreis.columns]

by_landkreis.to_csv('../data/rki_to_jhu.csv')
