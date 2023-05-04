import pandas as pd
import geopandas as gpd
import numpy as np
from numpy.linalg import norm
import requests as req
from bs4 import BeautifulSoup
import json
import re
from matplotlib import pyplot as plt


def read_json_data(path, epsg=4326, loc_cols=['lng', 'lat'], drop_duplicates=False):
    """
    Read the json data and return a geopandas dataframe
    """
    df = pd.read_json(path)
    if drop_duplicates:
        df.drop_duplicates(inplace=True)
    df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(
        df[loc_cols[0]], df[loc_cols[1]]))
    df.set_crs(epsg=epsg, inplace=True)
    return df


def set_zone(yoshi, radius=500):
    """
    Set the zone for the dataframe
    """
    yoshi = yoshi.to_crs(epsg=2326)
    yoshi['zone'] = yoshi.buffer(radius).to_crs(epsg=4326)
    yoshi = yoshi.to_crs(epsg=4326)
    return yoshi


def concat_geometry(dfs):
    return pd.concat([df.geometry for df in dfs], ignore_index=True)


def get_features_by_location(yoshi: gpd.GeoDataFrame, candiates_location: gpd.GeoSeries):
    """
    Get the features by location
    """
    common_index = candiates_location.apply(
        lambda location: location.within(yoshi.geometry).argmax())
    new_df = yoshi.loc[common_index]
    new_df.index = candiates_location.index
    return new_df.select_dtypes(include=np.number)


def cosine_similarity(candidate_feature: pd.DataFrame, target_feature: pd.Series):
    """
    Calculate the cosine similarity between two vectors
    """
    return candidate_feature.apply(lambda row: np.dot(row, target_feature)/(norm(row)*norm(target_feature)), axis=1)


def minmaxnorm(x):
    """
    Minmax normalization
    """
    return (x-x.min())/(x.max()-x.min())


def minmax_normalize(geodf: gpd.GeoDataFrame):
    """
    Normalize the dataframe
    """
    geom = geodf.geometry
    geodf = pd.DataFrame(geodf.select_dtypes(include=np.number))
    geodf = minmaxnorm(geodf)
    geodf = gpd.GeoDataFrame(geodf, geometry=geom)
    return geodf


def min_distance(candidates_location: gpd.GeoSeries, yoshi: gpd.GeoDataFrame):
    candidates_location = candidates_location.to_crs(epsg=2326)
    yoshi = yoshi.to_crs(epsg=2326)
    return candidates_location.apply(lambda location: yoshi.distance(location).min())


def get_density(df: gpd.GeoDataFrame, col: str):
    """
    Get the density of the column
    """
    return df[col]/df.to_crs(epsg=6933).area


def create_features(dcca: gpd.GeoDataFrame):
    dcca['t_tmmearn'] = dcca.t_mmearn*dcca.t_wp
    dcca["den_pop"] = get_density(dcca, "t_pop")
    dcca["den_income"] = dcca.t_mmearn*dcca.den_pop


def dms_to_decimal(dms):
    deg, minutes, seconds, direction = re.split('[^A-Za-z0-9]', dms)
    decimal_degrees = float(deg) + float(minutes)/60 + float(seconds)/(60*60)
    if direction in ['W', 'S']:
        decimal_degrees *= -1
    return decimal_degrees


def get_station_list():
    index_url = "https://en.wikipedia.org/wiki/List_of_MTR_stations"
    response = req.get(index_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    a_list = soup.select(
        "#mw-content-text > div.mw-parser-output > table > tbody > tr > td:nth-child(2) > a")
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
        print("get:", url)
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
        station["title"] = station["title"].replace(
            "(MTR)", "").replace("station", "").strip()
    return station_list
