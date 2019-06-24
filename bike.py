#!flask/bin/python
import csv, sys, gmplot, numpy as np,  matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

dict_list = []
def loadData():
    filename = "201904-fordgobike-tripdata.csv"
    with open(filename) as data:
        reader = csv.DictReader(data)
        for line in reader:
            dict_list.append(line)

def station_to_coordinates():
    dictionary = dict()
    for entry in dict_list:
        if entry["start_station_name"] not in dictionary:
            dictionary[entry["start_station_name"]] = {"lat": float(entry["start_station_latitude"]), "lng": float(entry["start_station_longitude"])}
    # print(dictionary)
    return dictionary

# def getEndsForTarget(target):
#     lat = 0
#     lon = 0
#     end_lats = []
#     end_lons = []
#     print(target)   
#     for entry in dict_list:
#         if entry["start_station_name"] == target:
#             end_lats.append(float(entry["end_station_latitude"]))
#             end_lons.append(float(entry["end_station_longitude"]))
#             lat = float(entry["start_station_latitude"])
#             lon = float(entry["start_station_longitude"])
#     return lat, lon, end_lats, end_lons


def getStartsForTarget(target):
    lat = 0
    lon = 0
    end_lats = []
    end_lons = []
    print(target)   
    for entry in dict_list:
        if entry["end_station_name"] == target:
            end_lats.append(float(entry["start_station_latitude"]))
            end_lons.append(float(entry["start_station_longitude"]))
            lat = float(entry["end_station_latitude"])
            lon = float(entry["end_station_longitude"])
    return lat, lon, end_lats, end_lons

# def getStartsForTargetByCoords(lat, lon):
#     end_lats = []
#     end_lons = []
#     for entry in dict_list:
#         if entry["end_station_latitude"] == lat and entry["end_station_longitude"] == lon:
#             end_lats.append(float(entry["start_station_latitude"]))
#             end_lons.append(float(entry["start_station_longitude"]))
#     return end_lats, end_lons


# @app.route('/findEndStations')
# def findByStartStation():
#     stationName = request.args.get('stationName')
#     return make_map_start(stationName)

@app.route('/findStartStations')
def findByEndStation():
    stationName = request.args.get('stationName')
    zoom = request.args.get('zoom')
    if zoom == None:
        zoom = 13
    # if stationName == None:
    #     lat = request.args.get('lat')
    #     lon = request.args.get('lon')
    #     return make_map_end_coords(lat, lon)
    return make_map_end(stationName, zoom)


# def make_map_start(stationName):
#     print(stationName)
#     target_lat, target_lon, end_lats, end_lons = getEndsForTarget(stationName)
#     print(target_lat, target_lon)
#     stations = list(set([entry["start_station_name"] for entry in dict_list]))
#     return render_template('index.html', lat=target_lat, lon=target_lon, end_lats=end_lats, end_lons=end_lons, stationName=stationName, station_to_coordinates=station_to_coordinates())

def make_map_end(stationName, zoom):
    print(stationName)
    target_lat, target_lon, end_lats, end_lons = getStartsForTarget(stationName)
    print(target_lat, target_lon)
    stations = list(set([entry["start_station_name"] for entry in dict_list]))
    return render_template('index.html', lat=target_lat, lon=target_lon, end_lats=end_lats, end_lons=end_lons, stationName=stationName, station_to_coordinates=station_to_coordinates(), zoom=zoom)


# def make_map_end_coords(lat, lon):
#     end_lats, end_lons = getStartsForTargetByCoords(lat, lon)
#     stations = list(set([entry["start_station_name"] for entry in dict_list]))
#     return render_template('index.html', lat=lat, lon=lon, end_lats=end_lats, end_lons=end_lons, stationName=stationName, station_to_coordinates=station_to_coordinates())


if __name__ == '__main__':
    loadData()
    app.run()

# questions to answer 
# when do people ride
# where are pick ups / drop offs on the map
# most common routes?
# change over time? since it's sorted by month
# length of rides
# subscriber vs customer
# length of ride broken down by whether they're subscriber or customer?
# how old are people
# gender ratios



