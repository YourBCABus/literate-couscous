from datetime import datetime
import weather
import json
from pprint import pprint

# weather.main(datetime(2018, 8, 9))

with open('busdata.json', 'r') as f:
    data = json.load(f)

dates = []
datetimes = []

for item in data:
    print(item["time"])
    if item['time'][0:10] not in dates:
        dates.append(item['time'][0:10])
        datetimes.append(item['time'])

for date in datetimes:
    useDatetime = date.split('T')
    useDate = useDatetime[0].split('-')
    useTime = useDatetime[1].split(':')
    useDate = datetime(int(useDate[0]), int(useDate[1]), int(useDate[2]), min(int(useTime[0]), 23), int(useTime[1]), int(useTime[2][0:2]))
    weather.main(useDate)
