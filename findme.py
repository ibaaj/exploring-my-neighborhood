# -*- coding: utf-8 -*-

import requests
import json
import csv
from requests.auth import HTTPBasicAuth
from time import strftime

USERNAME = "XXXXXXX" # icloud username
PASSWORD = "XXXXXXX" # icloud pass

auth = HTTPBasicAuth(USERNAME, PASSWORD)
headers = {
    "Accept-Language":          "en-us",
    "Connection":               "keep-alive",
    "Content-Type":             "application/json; charset=utf-8",
    "User-agent":               "Find iPhone/1.3 MeKit (iPad: iPhone OS/4.2.1)",
    "X-Apple-Authscheme":       "UserIdGuest",
    "X-Apple-Find-Api-Ver":     "2.0",
    "X-Apple-Realm-Support":    "1.0",
    "X-Client-Name":            "iPad",
    "X-Client-UUID":            "MY_UUID",
}

res = requests.post("https://fmipmobile.icloud.com/fmipservice/device/%s/initClient" % USERNAME,
        auth=auth, data={}, headers=headers)

data = json.loads(res.text)

with open('/location.csv', 'a') as f:
    writer = csv.writer(f)
    # first launch : create columns' names
    #writer.writerow(["date","device","longitude","latitude","altitude"])
    for device in range(len(data["content"])):
        n = data["content"][device]["deviceModel"]
        lon = data["content"][device]["location"]["longitude"]
        lat = data["content"][device]["location"]["latitude"]
        alt = data["content"][device]["location"]["altitude"]
        writer.writerow([strftime("%Y-%m-%d %H:%M:%S"), n, lon, lat, alt])
