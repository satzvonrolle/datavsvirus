import requests
import pandas as pd

url_csv = "https://github.com/openZH/covid_19/tree/master/fallzahlen_kanton_total_csv/COVID19_Fallzahlen_Kanton_{}_total.csv"
cantons = ['AG', 'AI', 'AR', 'BE', 'BL', 'BS', 'FR', 'GE', 'GL', 'GR', 'JU', 'LU', 'NE', 'NW', 'OW', 'SG', 'SH', 'SZ', 'TG', 'TI', 'UR', 'VD', 'VS', 'ZG', 'ZH']

with requests.Session() as s:
    for canton in cantons:
        html = s.get(url_csv.format(canton))
        data = pd.read_html(html.content)[0]
        data.to_csv('../../data/raw/switzerland/Canton_{}.csv'.format(canton))

