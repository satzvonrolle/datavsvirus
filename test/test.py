import numpy as np
import pandas as pd

reference = pd.read_csv('../data/raw/reference.csv')
fused = pd.read_csv('../data/fused.csv')

for country in reference['Country/Region']:
    ref = reference.loc[reference['Country/Region'] == country]
    fus = fused.loc[fused['Country/Region'] == country]
    if not np.array_equal(ref.iloc[:, 4:].to_numpy(), fus.iloc[:, 4:].to_numpy()):
        print(f'Comparing {country}')
        ref_series = ref.sum()[4:]
        fus_series = fus.sum()[4:]
        diff_series = fus_series - ref_series
        print(diff_series)
