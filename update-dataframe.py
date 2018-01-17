#!/usr/bin/env python3
from os import sys
import os
sys.path.insert(0, '/usr/local/lib/python3.6')
sys.path.insert(0, os.path.expanduser('~/lib'))

import re
import pandas as pd
from typing import Dict, Optional
from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError
from os.path import isfile
from multiprocessing import Pool
from tqdm import tqdm


ip_db = Reader("GeoLite2-City.mmdb")


log_lines = []
with open("/var/log/auth.log") as log:
    log_lines = log.readlines()
print("Read {} lines from auth.log...".format(len(log_lines)))


def extract_row(line: str) -> Optional[Dict[str, str]]:
    if not "Failed" in line and not "invalid" in line.lower():
        return None
    ip = re.search("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", line)
    if not ip:
        return None
    username = re.search("for [A-Za-z]+ from", line)
    if not username:
        username = re.search("user [A-Za-z]+ from", line)
    if not username:
        return None
    keywords = line.split()
    time = " ".join(keywords[:3])
    server = keywords[3]
    try:
        ip_data = ip_db.city(ip.group(0))
    except AddressNotFoundError as e:
        print(e)
        return None
    row = {
        "Time": time,
        "Server": server,
        "IP": ip.group(0),
        "User": username.group(0).split()[1],
        "Continent": ip_data.continent.name,
        "Country": ip_data.country.name,
        "City": ip_data.city.name,
        "Subdivision": ip_data.subdivisions.most_specific.name,
        "Postcode": ip_data.postal.code,
        "Latitude": ip_data.location.latitude,
        "Longitude": ip_data.location.longitude,
    }
    return row


if isfile("data.csv"):
    df = pd.read_csv("data.csv")
else:
    df = pd.DataFrame()

print("Beginning line processor...")
with Pool(8) as p:
    new_data = [x for x in tqdm(p.imap_unordered(
        extract_row, log_lines), total=len(log_lines)) if x]
    new_data = pd.DataFrame(new_data, columns=["Time", "Server",        "IP",        "User",        "Continent",
                                               "Country",        "City",        "Subdivision",        "Postcode",        "Latitude",        "Longitude"])
df = pd.concat([new_data, df], ignore_index=True)
df.drop_duplicates(inplace=True)

print("Dumping CSV...")
df.to_csv("data.csv")
