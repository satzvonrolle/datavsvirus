import requests

url_csv = "https://raw.githubusercontent.com/openZH/covid_19/master/COVID19_Cases_Cantons_CH_total.csv"

with requests.Session() as s:
    file_csv = s.get(url_csv)
    with open('ch_data.csv', 'wb') as f:
        f.write(file_csv.content)
