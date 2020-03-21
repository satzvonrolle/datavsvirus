import pandas as pd
from datetime import datetime
from calendar import monthrange


STARTDATE = datetime(2020, 1, 22)
ENDDATE = datetime(2020, 3, 20)

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

def add_province(all_data, province_data):

    prevdata = 0
    for year in range(2020, 2040): # Let's hope there is no Corona anymore in 2040
        for month in range(1,13):
            for day in range(1, monthrange(year, month)[1]+1):
                print(year,month,day)
                thedate = datetime(year, month, day)
                
                if thedate>STARTDATE and thedate<ENDDATE:
                    dkey = str(month)+"/"+str(day)+"/"+str(year)
                    if dkey not in province_data:
                        province_data[dkey] = prevdata
                    else:
                        prevdata = province_data[dkey]
                        
                    
    all_data.append(province_data)

    
for row in data_rki.itertuples():
    
    if row.Landkreis != last_province: 
        if len(province_data)>0:

            add_province(all_data, province_data)

        last_province = row.Landkreis
        province_data = {}
        total_cases = 0
        province_data["State"] = "Germany"
        province_data["Province"] = row.Landkreis+", "+ row.Bundesland
   
        print(last_province)
    

    total_cases += row.AnzahlFall
    
    entry_date = datetime.utcfromtimestamp(int(row.Meldedatum/1000))
    
    if entry_date>STARTDATE and entry_date<ENDDATE:
        province_data[entry_date.strftime('%-m/%-d/%Y')] = total_cases
    
    print(datetime.utcfromtimestamp(int(row.Meldedatum/1000)).strftime('%Y-%m-%d %H:%M:%S'))

add_province(all_data, province_data) # add last province, which is not covered in loop

df_new = pd.DataFrame([x for x in all_data])

df_new.to_csv("../data/data_fused_rki.csv") 

