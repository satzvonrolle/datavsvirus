import pandas as pd
from datetime import datetime
import calendar
cal = calendar.Calendar()

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
# Iterate through all rows and reformat rows
#

last_province = ""
province_data = []
all_data = []
total_cases = 0

for row in data_rki.itertuples():
    
    if row.Landkreis != last_province: # TODO: Do not forget last province!
        if len(province_data)>0:
            # if a date is not in the list, use data from previous date
            prevdata = 0
            for month in [1,2,3,4]: # TODO: Change this to less hacky data
                for day in cal.itermonthdays(2020, month):
                    dkey = str(month)+"/"+str(day)+"/2020"
                    if dkey not in province_data:
                        province_data[dkey] = prevdata
                    else:
                        prevdata = province_data[dkey]
                        
                        
            all_data.append(province_data)

        last_province = row.Landkreis
        province_data = {}
        total_cases = 0
        province_data["State"] = "Germany"
        province_data["Province"] = row.Landkreis+", "+ row.Bundesland
        

        
        
    
        print(last_province)
    
    #TODO: if not row.AnzahlFall.isna():
    total_cases += row.AnzahlFall
        
    province_data[datetime.utcfromtimestamp(int(row.Meldedatum/1000)).strftime('%-m/%-d/%Y')] = total_cases
    
    print(datetime.utcfromtimestamp(int(row.Meldedatum/1000)).strftime('%Y-%m-%d %H:%M:%S'))


df_new = pd.DataFrame([x for x in all_data])

