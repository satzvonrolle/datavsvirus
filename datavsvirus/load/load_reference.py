import requests

base_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

# for key in ["Confirmed", "Deaths", "Recovered"]:
#     r = requests.get(base_url + "time_series_19-covid-"+key+".csv")  
#     with open('jhu_data_'+key+'.csv', 'wb') as f:
#         f.write(r.content)

r = requests.get(base_url + 'time_series_19-covid-Recovered.csv')  
with open('../../data/raw/reference.csv', 'wb') as f:
    f.write(r.content)
