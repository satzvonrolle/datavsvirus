import requests


for key in ["Confirmed", "Deaths", "Recovered"]:
    r = requests.get("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-"+key+".csv")  
    with open('jhu_data_'+key+'.csv', 'wb') as f:
        f.write(r.content)
