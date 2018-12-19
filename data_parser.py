import numpy as np
import pandas as pd
from datetime import datetime
import pytz
import json
import math

localtime = pytz.timezone("America/New_York")

# get data from json files
busdf_org = pd.read_json("busdata.json")
weatherdf = pd.read_json("weather.json")
with open("maps.json", "r") as mapsjson:
    mapsdata = json.load(mapsjson)
distances = pd.DataFrame({"distance": mapsdata})

# make new array with bus_id column
busdf = pd.DataFrame()
busdf["bus_id"] = busdf_org["bus_id"].apply(lambda x: int(x, 16))

# get list of dates in weather data
dates = [str(i)[0:10] for i in list(weatherdf)]

bustimedict = {}

# add weather details
for i in range(busdf_org.shape[0]):
    bus_id = busdf_org.at[i, "bus_id"]

    date = busdf_org.at[i, "time"][0:10]
    colData = str(weatherdf[date].values)[1:-1].split(" ")
    for j in range(len(colData)):
        busdf.at[i, j] = float(colData[j])

    busdf.at[i, "dist"] = distances.at[bus_id, "distance"]

    time = busdf_org.at[i, "time"][11:-5].replace(":", "")
    if int(time) < 190000:
        busdf.at[i, "halfday"] = 1
        time = int(time) + 34000
    else:
        busdf.at[i, "halfday"] = 0

    # magic
    date = localtime.localize(datetime.strptime(busdf_org.at[i, "time"], "%Y-%m-%dT%H:%M:%S.%fZ"))
    time = date.hour * 60 * 60 + date.minute * 60 + date.second + date.dst().total_seconds()
    # print(math.floor(time / (60 * 60)) - 5) THAT INCIDENT

    for j in range(5):
        key = "previous_%d" % (j + 1)
        try:
            array = bustimedict[bus_id]
            busdf.at[i, key] = array[len(array) - j - 1]
        except IndexError:
            busdf.at[i, key] = 0
        except KeyError:
            busdf.at[i, key] = 0

    if bus_id not in bustimedict:
        bustimedict[bus_id] = []

    bustimedict[bus_id].append(time)

    busdf.at[i, "time"] = time

# last column is predicted feature (time, GMT; format: hhmmss)
busdf.to_csv("data.csv")
