import json
import math

import requests
import mapsapi

towns = ["Allendale",
         "Alpine/Bergenfield Washington",
         "Becton/Carlstadt/East Rutherford",
         "Bergenfield High School",
         "Bogota",
         "Cliffside Park/Fairview/Pal Park",
         "Closter/Demarest",
         "Cresskill/Dumont",
         "Elmwood Park",
         "Emerson/Oradell/River Edge",
         "Englewood",
         "Englewood Cliffs",
         "Fair Lawn",
         "Fort Lee",
         "Franklin Lakes/Wyckoff BA9",
         "Franklin Lakes/Wyckoff BA10",
         "Garfield",
         "Glen Rock",
         "Harrington Park/Haworth",
         "Hasbrouck Heights",
         "Hillsdale/River Vale",
         "Hohokus/Saddle River",
         "Leonia",
         "Edgewater",
         "Lodi",
         "Lyndhurst/N Arlington/Wallington",
         "Mahwah East",
         "Mahwah West",
         "Maywood/Rochelle Park",
         "Midland Park/Waldwick",
         "Montvale",
         "New Milford",
         "Oakland/Fr Lakes/Wyck BA8",
         "Old Tappan/Northvale",
         "Paramus East",
         "Paramus West",
         "Park Ridge/Woodcliff Lake",
         "Ramsey",
         "Ridgefield",
         "Ridgefield Park/Little Ferry",
         "Ridgewood",
         "Rutherford",
         "Saddle Brook",
         "Teaneck",
         "Tenafly",
         "Upper Saddle River",
         "Washington Township/Westwood",
         "Teterboro/Moonachie/So Hackensack"]


def getBusID(town):
    r = requests.get("https://db.yourbcabus.com/schools/5bca51e785aa2627e14db459/buses")
    r_obj = json.loads(r.text)
    for i in range(len(r_obj)):
        if r_obj[i]["name"] == town:
            return r_obj[i]["_id"]
    return "null"


for town in towns:
    ltowns = town.split("/")
    total = 0
    for ltown in ltowns:
        total += mapsapi.main(ltown + "+NJ")
    average = math.floor(total/len(ltowns))
    mapsapi.addToFile(average, getBusID(town))

