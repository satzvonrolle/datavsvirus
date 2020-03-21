import pandas as pd

df = pd.read_csv('../data/jhu_data_Confirmed.csv')
italy = df.loc[(df['Country/Region'] == 'Italy')]
test1 = italy.sum()[4:]

df_merged = pd.read_csv('../data/jhu_data_Confirmed_with_Italy.csv')
italy_merged = df_merged.loc[(df_merged['Country/Region'] == 'Italy')]
test2 = italy_merged.sum()[4:]

test1 - test2
