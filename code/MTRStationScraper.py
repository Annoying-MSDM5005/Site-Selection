"""
MTRStationScraper.py
Author: Algebra-FUN
Copyright © 2023 All Rights Reserved.
"""


import requests as req
from bs4 import BeautifulSoup
import json
import re
import geopandas as gpd
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os

def dms_to_decimal(dms):
    deg, minutes, seconds, direction =  re.split('[^A-Za-z0-9]', dms)
    decimal_degrees = float(deg) + float(minutes)/60 + float(seconds)/(60*60)
    if direction in ['W', 'S']:
        decimal_degrees *= -1
    return decimal_degrees

def get_station_list():
    index_url = "https://en.wikipedia.org/wiki/List_of_MTR_stations"
    response = req.get(index_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    a_list = soup.select("#mw-content-text > div.mw-parser-output > table > tbody > tr > td:nth-child(2) > a")
    station_list = [a.attrs for a in a_list]
    return station_list

def find_station_longlat(url):
    response = req.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    lat = soup.select_one("span.latitude").text
    long = soup.select_one("span.longitude").text
    return {"lat": lat, "long": long}

def get_stations_info():
    station_list = get_station_list()
    for station in station_list:
        url = f"https://en.wikipedia.org{station['href']}"
        print("get:",url)
        latlong = find_station_longlat(url)
        station.update(latlong)
    return station_list

def preprocess(station_list):
    for station in station_list:
        try:
            station["lat"] = dms_to_decimal(station["lat"])
            station["long"] = dms_to_decimal(station["long"])
        except:
            pass
        station["title"] = station["title"].replace("(MTR)", "").replace("station", "").strip()
    return station_list