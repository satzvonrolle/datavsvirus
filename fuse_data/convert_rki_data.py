import pandas as pd
from datetime import datetime

#
# Load the RKI dataset and sort by Landkreis (province), Meldedatum (date) in order to generate time resolved data
#

data_rki = pd.read_csv("../data/rki_daten.csv").sort_values(by=['Landkreis', 'Meldedatum'])

#
# Retrieve possible ranges of dates. JHU data starts at January 22
#

dateset = []
for row in data_rki.itertuples():
    dateset.append(datetime.utcfromtimestamp(int(row.Meldedatum/1000)).strftime('%Y%m%d'))

print("All dates",set(dateset), "Min Date", min(dateset), "Max Date", max(dateset))


#
# TODO: Iterate through all rows and reformat rows
#

last_province = ""
province_data = []

for row in data_rki.itertuples():
    
    if row.Landkreis != last_province:
        last_province = row.Landkreis
        print(last_province)
        
    
    print(datetime.utcfromtimestamp(int(row.Meldedatum/1000)).strftime('%Y-%m-%d %H:%M:%S'))


