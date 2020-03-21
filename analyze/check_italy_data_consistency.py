import pandas as pd

df = pd.read_csv('../data/jhu_data_Confirmed_with_Italy.csv')

italy = df.loc[(df['Country/Region'] == 'Italy')]

test1 = italy.iloc[0][4:]
test2 = italy.iloc[1:].sum()[4:]

print(test1-test2)