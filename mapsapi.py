import json
import pprint
from datetime import datetime
import requests
import os


def get_key(filename="mapsapikey.txt"):
    # first line should be the api key
    return open(filename, "r").read()


def get_data(destination):
    key = get_key()

    # Polyline encoding for BCA
    origin = "enc:iqsxFfyzbM:"

    r = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&key=%s" % (origin, destination, key))
    r_obj = json.loads(r.text)
    return r_obj


def dealWithTheData(response):
    output = 0
    output = response["rows"][0]["elements"][0]["distance"]["value"]
    return output


def addToFile(data, busid):
    f = open("maps.json", "a")
    f.seek(f.tell() - 1, os.SEEK_SET)
    f.truncate()

    # this assumes that maps.json already contains something
    # if it is empty, add "{}" to it, run the script and then remove the leading comma
    toWrite = ", \"" + busid + "\": " + str(data) + "}"

    f.write(toWrite.replace("'", "\""))
    f.close()


def main(location):
    response = get_data(location)
    return dealWithTheData(response)


if __name__ == "__main__":
    main("200+Hackensack+Ave+Hackensack+NJ")