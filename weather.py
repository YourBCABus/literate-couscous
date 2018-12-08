import json
import pprint
from datetime import datetime
import requests
import os


def get_key(filename="keys.txt"):
    # first line should be the api key
    return open(filename, "r").read()


def get_data(day):
    key = get_key()

    # coordinates for BCA
    latitude = 40.9014937
    longitude = -74.034276

    r = requests.get("https://api.darksky.net/forecast/%s/%f,%f,%s" % (key, latitude, longitude, str(day).replace(" ", "T")))
    r_obj = json.loads(r.text)
    return r_obj


def dealWithTheData(response):
    output = {}
    stuffs = ["cloudCover", "humidity", "precipIntensity", "precipProbability", "precipType", "visibility", "windSpeed"]
    trimmedResponse = response["daily"]["data"][0]

    for stuff in stuffs:
        if stuff in trimmedResponse:
            if stuff == "precipType":
                output[stuff] = {"": 0, "rain": 1, "snow": 2, "sleet": 3}[trimmedResponse[stuff]]
            else:
                output[stuff] = trimmedResponse[stuff]
        else:
            output[stuff] = 0

    output["sunsetTime"] = str(datetime.fromtimestamp(response['daily']['data'][0]["sunsetTime"]))[11:].replace(":", "")
    return output


def addToFile(data, day):
    f = open("weather.json", "a")
    f.seek(f.tell() - 1, os.SEEK_SET)
    f.truncate()

    # this assumes that weather.json already contains something
    # if it is empty, add "{}" to it, run the script and then remove the leading comma
    toWrite = ", \"" + str(day)[0:10] + "\": " + str(data) + "}"

    f.write(toWrite.replace("'", "\""))
    f.close()


def main(date):
    response = get_data(date)
    data = dealWithTheData(response)
    addToFile(data, date)


if __name__ == "__main__":
    main(datetime(2007, 12, 4))
