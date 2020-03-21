import requests
r = requests.get("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")  
with open('data/jhu_data.csv', 'wb') as f:
    f.write(r.content)
