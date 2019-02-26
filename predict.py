from __future__ import print_function

import requests
import datetime
import json
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pytz
import random

localtime = pytz.timezone("America/New_York")
date = datetime.date.today()

if date.weekday() == 5 or date.weekday() == 6:
    exit(0)

weather_cols = ["cloudCover"]

ybb_key = open("yourbcabuskey.txt", "r").read()

def noop():
    return

def get_dark_sky_key(filename="darkskyapikey.txt"):
    # first line should be the api key
    return open(filename, "r").read()

def get_weather_data():
    key = get_dark_sky_key()

    # coordinates for BCA
    latitude = 40.9014937
    longitude = -74.034276

    r = requests.get("https://api.darksky.net/forecast/%s/%f,%f" % (key, latitude, longitude))
    r_obj = json.loads(r.text)
    return r_obj

def dealWithTheData(response):
    output = {}
    trimmedResponse = response["daily"]["data"][0]

    for stuff in weather_cols:
        if stuff in trimmedResponse:
            if stuff == "precipType":
                output[stuff] = {"": 0, "rain": 1, "snow": 2, "sleet": 3}[trimmedResponse[stuff]]
            else:
                output[stuff] = trimmedResponse[stuff]
        else:
            output[stuff] = 0

    output["sunsetTime"] = str(datetime.datetime.fromtimestamp(response['daily']['data'][0]["sunsetTime"]))[11:].replace(":", "")
    return output

# Defines the model
def build_model():
    model = keras.Sequential([
        keras.layers.Dense(8, activation=tf.nn.relu,
                           input_shape=(8,)),
        keras.layers.Dense(7, activation=tf.nn.relu),
        keras.layers.Dense(6, activation=tf.nn.softmax)
    ])

    optimizer = tf.train.AdamOptimizer()

    model.compile(loss="categorical_crossentropy",
                  optimizer=optimizer,
                  metrics=["mae"])

    return model

# Uses the model
model = build_model()
model.load_weights("model.h5")

weather_data = dealWithTheData(get_weather_data())
print("Cloud cover:")
print(weather_data["cloudCover"])

with open("maps.json", "r") as mapsjson:
    mapsdata = json.load(mapsjson)

bins = [-150, 150, 450, 750, 1050, 1200]
mean = np.array([6.08480176e-01, 1.62408238e+04, 1.29955947e-01, 7.17457269e+04, 7.15527588e+04, 6.94075925e+04, 6.87244306e+04, 6.64467709e+04])
std = np.array([2.67124727e-01, 1.68540390e+04, 3.36254961e-01, 1.53221963e+04, 1.53749422e+04, 2.04633288e+04, 2.04714894e+04, 2.44829247e+04])

invalidate = datetime.datetime(date.year, date.month, date.day, 23, 59, 59)

buses = requests.get("https://db.yourbcabus.com/schools/5bca51e785aa2627e14db459/buses").json()
i = 0
for bus in buses:
    history = requests.get("https://db.yourbcabus.com/schools/5bca51e785aa2627e14db459/buses/%s/last10" % bus["_id"]).json()
    previous = [0, 0, 0, 0, 0]
    i = 0
    j = 0
    while i < 5:
        try:
            date = localtime.localize(datetime.datetime.strptime(history[j]["time"], "%Y-%m-%dT%H:%M:%S.%fZ"))
            j = j + 1
            time = date.hour * 60 * 60 + date.minute * 60 + date.second + date.dst().total_seconds()
            if time > 19 * 60 * 60:
                previous[i] = time
                i = i + 1
        except IndexError:
            break
        except KeyError:
            break

    x = (np.array([[weather_data["cloudCover"], mapsdata[bus["_id"]] or 0, 0, *previous]]) - mean) / std
    result = bins[int(np.argmax(model.predict(x)))]

    r = requests.patch("https://db.yourbcabus.com/schools/5bca51e785aa2627e14db459/buses/%s" % bus["_id"], data = json.dumps({
        "boarding": result,
        "locations": [],
        "invalidates": invalidate.isoformat() + "Z"
    }), headers = {"Authorization": "Basic %s" % ybb_key})
    print("%s: %d" % (bus["name"], result))
