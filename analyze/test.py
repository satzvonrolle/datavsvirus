import pandas as pd

jhu = pd.read_csv('../data/jhu_data_Confirmed.csv')

jhu_germany = jhu.loc[(jhu['Country/Region'] == 'Italy')].sum()[4:]
jhu_italy = jhu.loc[(jhu['Country/Region'] == 'Italy')].sum()[4:]

df = pd.read_csv('../data/jhu_data_Confirmed_with_Italy.csv')
df_italy = df.loc[(df['Country/Region'] == 'Italy')].sum()[4:]

italy = jhu_italy - df_italy

