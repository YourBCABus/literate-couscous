import numpy as np
import pandas as pd
from datetime import datetime
import pytz

# Define a time zone because of freakin' DST!!! *gah*
localtime = pytz.timezone("America/New_York")
# Yes, I felt the need to make not 1, but 2 whole comments for this one line!!
# Hey, it's me commenting from like 10 minutes later, and now I feel the need to bring this up again.
# I don't like working with dates. Who even decided that this stuff was a good idea? **AAARGLE**
# Okay, now, at like 15 minutes from the previous one, now 5 comments
# 6: Feel free to delete this later
# 7: </rant>

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
        busdf.at[i, j] = float(colData[j])

    time = busdf_org.at[i, "time"][11:-5].replace(":", "")
    if int(time) < 190000:
        busdf.at[i, "halfday"] = 1
        time = int(time) + 34000
    else:
        busdf.at[i, "halfday"] = 0

    # You know, by this point, I don't even care anymore about the next line's readability
    time = int(time) + int(str(localtime.localize(datetime.strptime(busdf_org.at[i, "time"], "%Y-%m-%dT%H:%M:%S.%fZ")).dst()).replace(":", ""))
    # print(time)
    # Honestly, it isn't *too* bad... only 143 characters
    # Yes, I could have made this more concise, but why bother at this point? It *should* work.
    # I mean, I think it does. That's fine, right?

    busdf.at[i, "time"] = time

# the last column, "time", is the final arrival time if it were a normal day (day ends at 4:10)
# any times before 2pm EST (7pm GMT) will have an extra 3hrs 40min added (12:30 to 4:10)
# adds an hour if it needs to for DST using pytz
# bus locations have not been added
# instead, they can be estimated using arrival time predictions
busdf.to_csv("data.csv")
