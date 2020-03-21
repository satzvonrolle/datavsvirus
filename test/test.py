import numpy as np
import pandas as pd

reference = pd.read_csv('../data/raw/reference.csv')
fused = pd.read_csv('../data/fused.csv')

for country in reference['Country/Region']:  # country = 'Italy'
    ref = reference.loc[reference['Country/Region'] == country]
    fus = fused.loc[fused['Country/Region'] == country]
    if not np.array_equal(ref.to_numpy()[:, 4:].astype(float), fus.to_numpy()[:, 4:].astype(float)):
        print(f'Comparing {country}')
        ref_series = ref.sum()[4:]
        fus_series = fus.sum()[4:]
        diff_series = fus_series - ref_series
        print(diff_series)

# # loop

# jhu_germany = jhu.loc[(jhu['Country/Region'] == 'Italy')].sum()[4:]
# jhu_italy = jhu.loc[(jhu['Country/Region'] == 'Italy')].sum()[4:]

# df = pd.read_csv('../data/jhu_data_Confirmed_with_Italy.csv')
# df_italy = df.loc[(df['Country/Region'] == 'Italy')].sum()[4:]

# italy = jhu_italy - df_italy
