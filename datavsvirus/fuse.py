import pandas as pd
import os

global_df = pd.read_csv('../data/raw/reference.csv')

for country in [name for name in os.listdir('../data/converted') if name.endswith('.csv')]:
    print(f'fusing {country}')
    country_df = pd.read_csv(f'../data/converted/{country}')
    global_df = global_df.drop(global_df.loc[global_df['Country/Region'] == country[:-4].capitalize()].index)
    global_df = pd.concat([global_df, country_df], ignore_index=True)

global_df.to_csv('../data/fused.csv', index=False)
