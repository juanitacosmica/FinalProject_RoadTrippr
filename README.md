TrippR
======

# Table of Contents

1. [Overview](#Overview)
2. [Background](#Background)
3. [Objective](#Objective)
4. [How It Works](#how-it-works)
5. [Data Research](#data-research)
6. [Related Work](#related-work)
7. [Challenges](#challenges)
8. [Improvements](#improvements)

# Overview

TrippR is a navigation and travel recommendation app.

(See our __presentation:__ <https://bit.ly/3FJNgXG>)

## Background

According to a recent survey of road travelers in the US, more than three-quarters (78%) of Americans have found hidden gems along the road that they would not have seen if they were traveling another way. More than one-third (35%) said they prefer a mix of both planned and unexpected stops. Currently even the best travel recommendation apps do not optimize for route and even the best navigation apps do not optimize for the relevance and quality of the experience. TrippR does both, as well as provides high-rating recommendations based on the user profile.

## Objective

To generate the most relevant travel itinerary (3 stops) based on starting location and destination information according to a user's profile. 
- To create an itinerary and to display a map with the waypoints and route.

# How it Works

A ML-driven recommendation algorithm powered by Google APIs. A profile is created for users based on a short survey (10 questions) which can provide the most relevant travel suggestions between a departure and arrival destination.

### Travel preferences

Using a Google Reviews Dataset containing comprised of user ratings across 24 categories (which became 22 after dropping hotel and local services) of place `type`, we assemble clusters that represent a fingerprint of different traveler paradigms. These clusters act as a reasonable predictor of which attractions a user will like the most.

(_A past UCI [project](https://vasanth16.github.io/) and this dataset is [kindly provided by the UCI Machine Learning Repository at UC Irvine](https://archive.ics.uci.edu/ml/about.html)._)

### Recommendations

TrippR users register and answer an According to the user's profile the algorithm predicts how they would score each category of attraction and identifies the most highly rated locations. These are used to create the optimal travel itinerary based on the type of place and the route information. 

### Route Optimization

Stops in each itinerary are co-optimized for highest quality experience and efficient navigation between the starting and ending destination. _Initially_, only stops within a max of 25km of the intended route will be recommended and the number of stops is fixed at 3.

Navigation is essentially a graph problem. Places that are likely to be preferred by a particular user will be ranked more highly and considered more 'worth' visiting - at the same time other factors like driving distance, driving time, time of day, trip duration, and final destination also impact which places can be adequately visited during a particular trip. The challenge of this component is balancing the best quality itinerary while making recommendations that are still feasible. This represents an open door to future improvements of Trippr.

### Iterative reclustering

As users select more trips the recommendations should improve in precision and quality. User preferences are fed back into the model to improve the accuracy and segmentation of each of the groupings, and an individual user's selections are iterated to improve their most accurate assignment to the correct cluster. Which is a future improvement of Trippr.

## Technologies

* Google Maps
* Python
* Javascript
* SKlearn
* Firebase
* HTML + CSS
* MapQuest
* Py Script 
* Flask 

# Data Research

## In this section:

* ML training data
* info on relevant APIs
* info on available data and format
* next steps
* some of the projects we looked at

### Training data

In order to provide accurate travel recommendations, our algorithm needs to understand travel preferences then assign a profile to the user. We researched datasets on tourism preferences that would support the correct assignment of trip types and destinations. Categories of traveler should be able to be assembled based on a representative sample of recent and relevant travel preference information.

A [project](https://vasanth16.github.io/#Part-5:-Finding-Clusters-in-our-Data) which previously modelled based on this user ratings dataset k-means clustering. We saw other examples that employed, variously: naive Bayesian, neural network, deep learning, and PCA models. Some of them are referenced below in the [Related Work](#related-work) section.

### APIs

* Google APIs are our friend.

1. [Places API - Find A Place](https://developers.google.com/maps/documentation/places/web-service/search-find-place#find-place-responses)
2. [Place Details API](https://developers.google.com/maps/documentation/places/web-service/details) - Good when we want to add additional attractions by place `type` [parameter](https://developers.google.com/maps/documentation/places/web-service/supported_types#table1), such as `museum`, `art_gallery`, or `zoo`. Also supports reviews or `rating` as a way of marking how 'good' a particular attraction is.
3. [Directions API - route from A to B to C](https://developers.google.com/maps/documentation/directions/get-directions)
4. [Distance Matrix API - estimate travel time and distance for multiple destinations](https://developers.google.com/maps/documentation/distance-matrix/start) - on top of knowing the optimal route to get there, we need to understand how long the journey will take.

(longer description and response examples will follow)

__Limitations:__ 

* Max requests: Number of API requests goes up `O(n²)` as the number of destinations.
* Place Search vs. Nearby Search: [From Google API docs](https://developers.google.com/maps/documentation/places/web-service/search-nearby)
>Nearby Search and Text Search return all of the available data fields for the selected place (a subset of the supported fields), and you will be billed accordingly There is no way to constrain Nearby Search or Text Search to only return specific fields. To keep from requesting (and paying for) data that you don't need, use a Find Place request instead.
* License: Scraping and offline storage of Google Maps data is apparently _prohibited_ (from [Terms of Service](https://cloud.google.com/maps-platform/terms/#3-license)):
>3.2.3 Restrictions Against Misusing the Services. (a)  No Scraping. Customer will not export, extract, or otherwise scrape Google Maps Content for use outside the Services. For example, Customer will not: (i) pre-fetch, index, store, reshare, or rehost Google Maps Content outside the services; (ii) bulk download Google Maps tiles, Street View images, geocodes, directions, distance matrix results, roads information, places information, elevation values, and time zone details; (iii) copy and save business names, addresses, or user reviews; or (iv) use Google Maps Content with text-to-speech services.

# Related Work

The Trippr team reviewed other projects and resources that have previously done work in this domain. Some, but not all of them are linked below. Thanks to these authors!

## Using Google Reviews Data

Comparing Tourist Preferences in Asia and Europe (_Sam Childs and Vasanth Rajasekaran at UC Irvine_): <https://vasanth16.github.io/>

Travel Review Analysis (_Wirach Leelakiatiwong_): <https://www.kaggle.com/code/wirachleelakiatiwong/travel-review-analysis>

## Unsupervised Machine Learning Model

Three key factors played the role as to which Machine Learning Model should be used to best fit the Trippr needs:
- Choosing principal components
- The use of K-Means (vs. other methods)
- Accurate cluster assignment of users
KMeans was selected.

Reference: SmartTourister (_Salil Gautam, Shubham Verma, Nishant Gore_): https://github.com/salil-gtm/SmartTourister

## Recommendation Engine

After performing the KMeans with the Google Reviews Data and getting the clusters, we were able to give shape to the type of travelers using Trippr, and therefore based on their responses to questions that were carefully thought of, a weight is given, and each user can be allocated to a cluster.

From a relationship between their preferences (cluster the user falls in) and the highest rating places available, a data processing occurs and it throws the 3 stops for the travaller in a list.

## Navigation / route optimization

The list with the 3 stops goes to JS through Flask, and this plugs in then to MapQuest which will populate the route. 

- References:
Optimizing Travel Itineraries With Machine Learning (Vladimir Lazovskiy): <https://github.com/vlazovskiy/route-optimizer-machine-learning>
Computing Optimal Roadtrips on a Budget (_Randal Olson_): <https://github.com/rhiever/Data-Analysis-and-Machine-Learning-Projects/blob/master/pareto-optimized-road-trip/optimized-state-capitols-trip.ipynb>

Optimal Road Trips Across the World (_Randy Olson_): >https://github.com/rhiever/optimal-roadtrip-usa>
Road Trip Router (_Peter Sanders_): <https://github.com/hxtk/Road-Trip-Router>

## APIs Reference

Travel Advisor (_Adrian Hajdin_): <https://github.com/adrianhajdin/project_travel_advisor>

Awesome Travel (<https://github.com/unseen1980/awesome-travel>)

Tourism APIs <https://www.programmableweb.com/category/tourism/api>

# Challenges

- Limitation to user information data
- JS connection to Python
- Dataset (limited to a few free options such as: Google Review Data, Kaggle, amongst not many others) 

# Improvements
- Radius search (not being limited 25km or so, rather based on User's input, how far they prefer to go)
- Offer multiple sets of trip suggestions and provide an overview of the places being visited
- Save users' trip selections and reintegrate their decisions (reclustering/re-weighting)
- Improve onboarding questionnaire eg. tree of general Qs then more cluster-specific questions (multi-classification model); semantic models and relationship to cluster categories
- Use sentiment analysis