import pandas as pd
import glob



def read_data_ita(date):
    '''
    Reads csv-file with italien data by date in format day/month/year eg. '3/15/20'.
    Italien file format
                        data stato  codice_regione  denominazione_regione  codice_provincia denominazione_provincia sigla_provincia        lat       long  totale_casi
    0    2020-02-24 18:00:00   ITA              13                Abruzzo                69                  Chieti              CH  42.351032  14.167546            0
    1    2020-02-24 18:00:00   ITA              13                Abruzzo                66                L'Aquila              AQ  42.351222  13.398438            0

    removes lines containing 'In fase di definizione/aggiornamento'
    :return:
    pandas DataFrame
    '''

    new_date = date.split('/')
    day = int(new_date[0])
    month = int(new_date[1])
    fname = './ita_data_%02d%02d.csv' % (day, month)
    dataFrame = pd.read_csv(fname)
    data_ita = dataFrame[dataFrame['denominazione_provincia'] != 'In fase di definizione/aggiornamento']
    return data_ita


def read_data_jhu():
    data_jhu = pd.read_csv('./jhu_data_Confirmed.csv')
    return data_jhu

data_jhu = read_data_jhu()
date_list_jhu = list(data_jhu.columns[4:])
date_list_ita = glob.glob('./ita_data_*.csv')

date_list_merge = []
for fname in date_list_ita:
    month = int(fname.split('_')[-1].split('.')[0][:2])
    day = int(fname.split('_')[-1].split('.')[0][2:])
    date_list_merge.append('%d/%d/20' % (month, day))


start_index = data_jhu.index[-1] + 1
for i in range(107):
    data_jhu = data_jhu.append(pd.Series(name=data_jhu.index[-1]+1))
end_index = data_jhu.index[-1]


fname = date_list_ita[0]
month = fname.split('_')[-1].split('.')[0][:2]
day = fname.split('_')[-1].split('.')[0][2:]
date = '{}/{}/20'.format(month, day)
data_ita = read_data_ita(date)


for i, province, lat, long in zip(range(start_index, end_index+1),
                       list(data_ita['denominazione_provincia']),
                       list(data_ita['lat']),
                       list(data_ita['long'])
                       ):
    data_jhu.at[i, 'Province/State'] = province
    data_jhu.at[i, 'Country/Region'] = 'Italy'
    data_jhu.at[i, 'Lat'] = lat
    data_jhu.at[i, 'Long'] = long

for date in date_list_jhu:
    if date in date_list_merge:
        data_ita = read_data_ita(date)
        nmb_provinces = len(list(data_ita['denominazione_provincia']))
        if not nmb_provinces == 107:  # number of provinces should be equal the total number
            raise Exception('Number of provinces in %s not correct' % (date,))
        for i, total_cases in zip(range(start_index, end_index+1),
                                  list(data_ita['totale_casi'])):
            data_jhu.at[i, date] = total_cases
    else:
        for i in range(start_index, end_index+1):
            data_jhu.at[i, date] = 0

data_jhu.to_csv('./ita_merge.csv')





#Province/State                    Country/Region      Lat      Long  1/22/20  1/23/20  1/24/20  1/25/20  1/26/20  1/27/20  1/28/20  1/29/20  ...  3/9/20  3/10/20  3/11/20  3/12/20  3/13/20  3/14/20  3/15/20  3/16/20  3/17/20  3/18/20  3/19/20  3/20/20
# list(types[-1].columns)[4:]