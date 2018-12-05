from datetime import datetime
import weather
import json
from pprint import pprint

# weather.main(datetime(2018, 8, 9))

with open('busdata.json', 'r') as f:
    data = json.load(f)

dates = []

for item in data:
    if item['time'][0:10] not in dates:
        dates.append(item['time'][0:10])

for date in dates:
    useDate = date.split('-')
    useDate = datetime(int(useDate[0]), int(useDate[1]), int(useDate[2]))
    weather.main(useDate)
