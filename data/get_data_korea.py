import requests
import pandas as pd
import re

# get html strings of 10 most recent pages
pages = ['https://www.cdc.go.kr/board/board.es?mid=a30402000000&bid=0030&nPage={}'.format(p) for p in range(1, 10)]
content = ''
for page in pages:
    # print("Page {}".format(page))
    data = requests.get(page)
    content += data.content.decode('utf-8')

link = 'https://www.cdc.go.kr/board/board.es?mid=a30402000000&bid=0030&act=view&list_no={}&tag=&nPage=1'
days = range(31, 0, -1)  # backwards
months = [3, 2]  # March & February only for now

overview = []
regions = []
for month in months:
    for day in days:
        pattern = "goView\('(.+)'\);.+[uU]pdate.+COVID-19.+\n.+\n.+2020-{:02}-{:02}".format(month, day)
        match = re.search(pattern, content)
        if match is None:
            print("No match found for {} {}.".format(day, month))
            continue
        number = match.groups(0)[0]
        day_content = requests.get(link.format(number)).content
        try:
            day_db = pd.read_html(day_content.decode('utf-8'))
        except Exception as e:
            print("No tables found for {} {}".format(day, month))
            continue
        overview.append(day_db[0])
        if len(day_db) == 2:
            regions.append(day_db[1])
        else:
            regions.append(None)

