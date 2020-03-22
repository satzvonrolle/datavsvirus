import datetime as dt
import requests

today = dt.datetime.today().date()
base = dt.date(2020, 2, 24)
days_back = (today-base).days

# formated date_list
date_list = [(today - dt.timedelta(days=i)).strftime('%m%d') for i in range(days_back + 1)]

for key in date_list:
    r = requests.get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-2020" + key + ".csv")
    if r.status_code == 404: # if there is no data for today
        continue
    with open(f'../../data/raw/italy/italy_{key}.csv', 'wb') as f:
        f.write(r.content)
