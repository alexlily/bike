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
    return dictionary


def end_station_to_visits():
    dictionary = dict()
    for entry in dict_list:
        if entry["end_station_name"] not in dictionary:
            dictionary[entry["end_station_name"]] = 0
        dictionary[entry["end_station_name"]] += 1

    return [(key, dictionary[key]) for key in sorted(dictionary, key= lambda item: dictionary[item], reverse=True)]

def start_station_to_visits():
    dictionary = dict()
    for entry in dict_list:
        if entry["start_station_name"] not in dictionary:
            dictionary[entry["start_station_name"]] = 0
        dictionary[entry["start_station_name"]] += 1
    return [(key, dictionary[key]) for key in sorted(dictionary, key= lambda item: dictionary[item], reverse=True)]


def getCoordinates(target):
    lat = 0
    lon = 0
    target_lats = []
    target_lons = []
    for entry in dict_list:
        if entry["end_station_name"] == target:
            target_lats.append(float(entry["start_station_latitude"]))
            target_lons.append(float(entry["start_station_longitude"]))
            lat = float(entry["end_station_latitude"])
            lon = float(entry["end_station_longitude"])
    return lat, lon, target_lats, target_lons


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/findStartStations')
def findByEndStation():
    stationName = request.args.get('stationName')
    zoom = request.args.get('zoom')
    if stationName not in station_to_coordinates():
        stationName = "San Francisco Caltrain Station 2  (Townsend St at 4th St)"  # set a default
    if zoom is None:
        zoom = 13
    return make_map(stationName, zoom)


@app.route('/pointsData')
def pointsData():
    stationName = request.args.get('stationName')
    lat, lon, target_lats, target_lons = getCoordinates(stationName)
    return json.dumps({
        "stationName": stationName,
        "lat": lat,
        "lon": lon,
        "target_lats": target_lats,
        "target_lons": target_lons
    })


@app.route('/popularDestination')
def sortByMostPopularDestination():
    return json.dumps(end_station_to_visits())


@app.route('/popularSource')
def sortByMostPopularSource():
    return json.dumps(start_station_to_visits())


def make_map(stationName, zoom):
    target_lat, target_lon, end_lats, end_lons = getCoordinates(stationName)
    return render_template('map.html', lat=target_lat, lon=target_lon, end_lats=end_lats,
        end_lons=end_lons, stationName=stationName, station_to_coordinates=station_to_coordinates(), 
        zoom=zoom)


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



