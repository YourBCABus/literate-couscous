import numpy as np
import pandas as pd
from datetime import datetime

# get data from json files
busdf_org = pd.read_json("busdata.json")
weatherdf = pd.read_json("weather.json")

# make new array with bus_id column
busdf = pd.DataFrame()
busdf["bus_id"] = busdf_org["bus_id"]
busdf["bus_id"] = busdf.bus_id.apply(lambda x: int(x, 16))

# get list of dates in weather data
dates = [str(i)[0:10] for i in list(weatherdf)]

# add weather details
for i in range(busdf_org.shape[0]):
    date = busdf_org.at[i, "time"][0:10]
    colData = str(weatherdf[date].values)[1:-1].split(" ")
    for j in range(len(colData)):
        busdf.at[i, j] = colData[j]

    time = busdf_org.at[i, "time"][11:-5].replace(":", "")
    if int(time) < 180000:
        busdf.at[i, "halfday"] = 1
    else:
        busdf.at[i, "halfday"] = 0
    busdf.at[i, "time"] = time

# the last column, "time", is the final arrival time
# bus locations have not been added
# instead, they can be estimated using arrival time predictions
busdf.to_csv("data.csv")
