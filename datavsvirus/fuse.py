import pandas as pd
import os

global_df = pd.read_csv('../data/raw/reference.csv')

for country in os.listdir('../data/converted'):
    country_df = pd.read_csv(f'../data/converted/{country}.csv')
    global_df = df.drop(df.loc[(global_df['Country/Region'] == country.capitalize()))
    global_df = pd.concat([global_df, country_df], ignore_index=True)

global_df.to_csv('../data/fused.csv', index=False)
