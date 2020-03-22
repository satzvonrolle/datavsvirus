import urllib
from zipfile import ZipFile
import os
import requests

script_dir = os.path.dirname(os.path.join(os.getcwd(), __file__))

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

if not yes_or_no("Please make sure usage is according to the license terms given in https://gadm.org/download_country_v3.html!"):
    exit()

data_dir = os.path.join(script_dir, '../geodata')

try:
    os.mkdir(data_dir)
except FileExistsError:
    pass

geodata_urls = ["https://biogeo.ucdavis.edu/data/gadm3.6/shp/gadm36_DEU_shp.zip", "https://biogeo.ucdavis.edu/data/gadm3.6/shp/gadm36_ITA_shp.zip"]

for url in geodata_urls:
    open(
        os.path.join(data_dir, url.split('/')[-1]),
        'wb'
    ).write(requests.get(url, allow_redirects=True).content)


for file in os.listdir(data_dir):
    with ZipFile(os.path.join(data_dir, file), 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall(path=data_dir)