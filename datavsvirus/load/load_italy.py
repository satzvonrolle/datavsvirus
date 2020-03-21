import requests

feb = ['02%02i' % i for i in range(24, 30)]
mar = ['03%02i' % i for i in range(1, 21)]

for key in feb + mar:
    r = requests.get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-2020" + key + ".csv")
    with open(f'../../data/raw/italy/italy_{key}.csv', 'wb') as f:
        f.write(r.content)
