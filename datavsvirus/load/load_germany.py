import pandas as pd
import requests

base_url = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'
offset = 0  # probably 2000 steps

rowbased = []

def make_request(base_url, offset=0):
    try:
        response = requests.get(base_url + f'&resultOffset={offset}')
    except:
        print('request failed')
    return response
    
for step in range(0, 8001, 2000):
    response = make_request(base_url, offset=step)
    for row in response.json()['features']:
        rowbased.append(row['attributes'])
        
pd.DataFrame(rowbased).to_csv('../../data/raw/germany/germany.csv')
