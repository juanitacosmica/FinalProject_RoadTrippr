# import dependencies
import numpy as np
from numpy.random import choice
import pandas as pd
import random
import requests
import json

# from config import gkey
from config.py import gkey

# TrippRoller uses the file called 'Weighted_Avg_Book.csv' generated by Weighted_Avgs.ipynb
ClusterAvgValues = pd.read_csv('Cluster_Weighting/Weighted_Avg_Book.csv')
ClusterAvgValues = ClusterAvgValues.drop('Unnamed: 0', 1)

# function to roll 1 activity, 1 sightseeing, 1 food according to cluster
def roll_trip(cluster, dest):

# need to pass cluster value here from user profile
    cluster = 0

    # roll an activity
    activity = list(ClusterAvgValues[['resort', 'beach', 'park', 'movie_theater', 'museum', 'shopping_mall', 'zoo', 'art_gallery', 'night_club', 'swimming-pools', 'gym', 'beauty-hair-spa']])
    activity_weights = np.array(ClusterAvgValues[['resort', 'beach', 'park', 'movie_theater', 'museum', 'shopping_mall', 'zoo', 'art_gallery', 'night_club', 'swimming-pools', 'gym', 'beauty-hair-spa']])
    cl_act_weights = activity_weights[cluster]
    normalized_act = cl_act_weights / cl_act_weights.sum()
    act_choice = choice(activity, p=normalized_act)

    # roll a sightseeing
    sightseeing = list(ClusterAvgValues[['place_of_worship', 'view-points', 'monument', 'gardens']])
    sightseeing_weights = np.array(ClusterAvgValues[['place_of_worship', 'view-points', 'monument', 'gardens']])
    cl_sight_weights = sightseeing_weights[cluster]
    normalized_sight = cl_sight_weights / cl_sight_weights.sum()
    sight_choice = choice(sightseeing, p=normalized_sight)

    # roll food&drink
    food = list(ClusterAvgValues[['restaurant', 'bar', 'burger-pizza', 'juice-bars', 'bakery', 'cafe']])
    food_weights = np.array(ClusterAvgValues[['restaurant', 'bar', 'burger-pizza', 'juice-bars', 'bakery', 'cafe']])
    cl_food_weights = food_weights[cluster]
    normalized_food = cl_food_weights / cl_food_weights.sum()
    food_choice = choice(food, p=normalized_food)

    trip_types = [act_choice, sight_choice, food_choice]

    radius = 3500
    # retrieve the destination from user input to get the location info
    dest = ""
    dest_url = ('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}').format(dest, gkey)
    dest_req = requests.get(dest_url).json()
    dest_lat = dest_req["results"][0]["geometry"]["location"]["lat"]
    dest_lng = dest_req["results"][0]["geometry"]["location"]["lng"]

    # use Places Nearby search to return the highest ranked of that `type` or `keyword`

    act_url = ("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={0}%2C{1}&radius={2}&keyword={3}&rankby=prominence&key={4}").format(dest_lat, dest_lng, radius, trip_types[0], gkey)
    act_req = requests.get(act_url).json()
    act_dest = ""
    if act_req["status"] == "ZERO_RESULTS":
        act_err = ("No {} results found in this area. Try a larger radius or a different activity.").format(trip_types[0])
        print(act_err)
    else:
        act_dest = [act_req["results"][0]["name"], act_req["results"][0]["vicinity"]]

    sight_url = ("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={0}%2C{1}&radius={2}&keyword={3}&rankby=prominence&key={4}").format(dest_lat, dest_lng, radius, trip_types[1], gkey)
    sight_req = requests.get(sight_url).json()
    sight_dest = ""
    if sight_req["status"] == "ZERO_RESULTS":
        sight_err = ("No {} results found in this area. Try a larger radius or a different activity.").format(trip_types[1])
        print(sight_err)
    else:
        sight_dest = [sight_req["results"][0]["name"], sight_req["results"][0]["vicinity"]]

    food_url = ("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={0}%2C{1}&radius={2}&keyword={3}&rankby=prominence&key={4}").format(dest_lat, dest_lng, radius, trip_types[2], gkey)
    food_req = requests.get(food_url).json()
    food_dest = ""
    if food_req["status"] == "ZERO_RESULTS":
        food_err = ("No {} results found in this area. Try a larger radius or a different activity.").format(trip_types[2])
        print(food_err)
    else:
        food_dest = [food_req["results"][0]["name"], food_req["results"][0]["vicinity"]]
    your_trip = [act_dest,
                sight_dest,
                food_dest]
    return your_trip