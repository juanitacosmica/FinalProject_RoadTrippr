TrippR
======

# Overview

TrippR is a navigation and travel recommendation app.

## Purpose

According to a recent survey of road travelers in the US, more than three-quarters (78%) of Americans have found hidden gems along the road that they wouldn't have seen if they were traveling another way. More than one-third (35%) said they prefer a mix of both planned and unexpected stops. Currently even the best travel recommendation apps don't optimize for route and even the best navigation apps don't optimize for the relevance and quality of experience. TrippR does both, as well as provides high-quality recommendations based on a user profile.

## The Goal

Generate the most relevant travel itinerary based on location and destination information according to a user's profile. Create an itinerary and display a map with the waypoints, route, and place information.

_Initially this is limited to_:
Offer 3 options for potential trips consisting of 3 destinations (up to 1:_attraction/sightseeing_; 1:_activity_; 1:_food_). Optimization for best route and highest preference are assumed at 25km.

# How it Works

An ML-driven recommendation algorithm powered by Google APIs. A profile is created for users based on a short survey which can then provide the most relevant travel suggestions between a departure and arrival destination.

(See our __presentation:__ <https://bit.ly/3FJNgXG>)

## In this section:

1. Travel Preferences
2. Recommendations
3. Iterative Reclustering
4. Route Optimization

### Travel preferences

Using a dataset containing comprised of user ratings across 24 categories of place `type` in Google and TripAdvisor reviews, we assemble clusters that represent a fingerprint of different traveler paradigms. These clusters act as a reasonable predictor of which attractions a user will like the most.

(_A [project](https://vasanth16.github.io/) and this dataset is [kindly provided by the UCI Machine Learning Repository at UC Irvine](https://archive.ics.uci.edu/ml/about.html)._)

### Recommendations

According to the user's profile the algorithm predicts how they would score each category of attraction and identifies the most highly rated locations. These are used to create the optimal travel itinerary based on the type of place and the route information. Users select from 3 recommended travel itineraries according to their preference.

### Route Optimization

Stops in each itinerary are co-optimized for highest quality experience and efficient navigation between the starting and ending destination. _Initially_, only stops within 25km of the intended route will be recommended.

### Iterative reclustering

As users select more trips the recommendations should improve in precision and quality. User preferences are fed back into the model to improve the accuracy and segmentation of each of the groupings, and an individual user's selections are iterated to improve their most accurate assignment to the correct cluster.

# Data Research

### In this section:

* ML training data
* info on relevant APIs
* info on available data and format
* next steps
* some of the projects we looked at

### Training data

In order to provide accurate travel recommendations, our algorithm needs to understand travel preferences then assign a profile to the user. We researched datasets on tourism preferences that would support the correct assignment of trip types and destinations. Categories of traveler should be able to be assembled based on a representative sample of recent and relevant travel preference information.

A [project](https://vasanth16.github.io/#Part-5:-Finding-Clusters-in-our-Data) which previously modelled based on this user ratings dataset k-means clustering. We saw other examples that employed, variously: naive Bayesian, neural network, deep learning, and PCA models.

### APIs

* Google APIs are our friend.

1. [Places API - Find A Place](https://developers.google.com/maps/documentation/places/web-service/search-find-place#find-place-responses)
2. [Place Details API](https://developers.google.com/maps/documentation/places/web-service/details) - Good when we want to add additional attractions by place `type` [parameter](https://developers.google.com/maps/documentation/places/web-service/supported_types#table1), such as `museum`, `art_gallery`, or `zoo`. Also supports reviews or `rating` as a way of marking how 'good' a particular attraction is.
3. [Directions API - route from A to B to C](https://developers.google.com/maps/documentation/directions/get-directions)
4. [Distance Matrix API - estimate travel time and distance for multiple destinations](https://developers.google.com/maps/documentation/distance-matrix/start) - on top of knowing the optimal route to get there, we need to understand how long the journey will take.

(longer description and response examples will follow)

### Trip Types

#### Parks

Opting to start with parks as a way of initially narrowing the scope of the route optimization problem. Parks data is provided by a variety of government and non-government APIs, some of which are explored below.

* National Parks

Parks Canada administers National Parks on a federal level. There are limitations to using _only_ national parks: there are [only 48 national parks and protected areas](https://ftp.geogratis.gc.ca/pub/nrcan_rncan/raster/atlas_6_ed/reference/eng/natpks_e.pdf "National Parks map") in total, and these are sparsely distributed, with many not road-accessible.

On the more complex end, Parks Canada does provide an API which can provide geospatial data in [Web Map Service (WMS)](https://www.nrcan.gc.ca/earth-sciences/geomatics/canadas-spatial-data-infrastructure/standards-policies/8938) format, however most Canadian national parks cover vast swaths of land area and the legislative boundary may overlap multiple provincial jurisdictions and lack a precise address able to be distilled into a single geographic point. More information on the [Canada Lands Administrative Boundaries Level 1 dataset can be found here](Canada Lands Administrative Boundaries Level 1 dataset).

As a simplified workaround, Parks Canada also provides basically an `.XML` dump listing the [names of all Canadian national parks and national historic sites](https://open.canada.ca/data/en/dataset/e0af6068-473b-4cd9-8cef-b2d98a05b368). This is simply a list of names but these can be extracted and used with other accompanying APIs, such as Google's [Places API](https://developers.google.com/maps/documentation/places/web-service/search-find-place) to populate the accurate `location` (`lat`,`lng`) and `adr_address` data, which is essential for those visiting the park by road (some parks have multiple [eg. East/West] entrances or multiple campgrounds which also might affect driving distance).

Example JSON output of Find Place responses:

```{
  "candidates":
    [
      {
        "formatted_address": "140 George St, The Rocks NSW 2000, Australia",
        "geometry":
          {
            "location": { "lat": -33.8599358, "lng": 151.2090295 },
            "viewport":
              {
                "northeast":
                  { "lat": -33.85824377010728, "lng": 151.2104386798927 },
                "southwest":
                  { "lat": -33.86094342989272, "lng": 151.2077390201073 },
              },
          },
        "name": "Museum of Contemporary Art Australia",
        "rating": 4.4,
      },
    ],
  "status": "OK",
}
```
More on Places and other Google APIs is discussed below.

* Provincial Parks

Parks authorities also administer the majority(?) of Canada's parks on a provincial level, for example Ontario parks oversees [343 provincial parks and protected areas](https://geohub.lio.gov.on.ca/datasets/c5191fcd8a944eaf91920b4ed914825a_4/explore?location=49.424602%2C-83.488646%2C3.88 "Map of Ontario Parks") along the following categories:
* Wilderness
* Nature Reserve
* Cultural Heritage
* Natural Environment
* Waterway
* Recreational

These are included in the following Land Information Ontario database: <https://geohub.lio.gov.on.ca/datasets/c5191fcd8a944eaf91920b4ed914825a/about>

This official registry also lacks the precise `location` and `address` information required to provide accurate road navigation directions, like we discussed in the section above, so syncing up this canonical list of parks with place data from companion APIs will be essential to populating an accurate database entry.

* All Campgrounds

On this road trip there are obviously more places to pitch a tent than just simply government-administered parks. For instance, there are over 500 conservation areas in Ontario (of which 300 are accessible to the public) and these are governed by [36 local Conservation Authorities](https://conservationontario.ca/conservation-authorities/find-a-conservation-authority "map of Ontario Conservation Authorities"). Moreover, there are countless unincorporated and private campgrounds that fall outside the administrative jurisdiction of these respective federal, provincial, and municipal bodies.

_Active Access_ provides Campground APIs that claim to "provide access to campground data for 97% of the US and Canada's national and state/provincial parks". These are:
* Campground API: <https://developer.active.com/docs/read/Campground_APIs>
* Campground Search API: <https://developer.active.com/docs/read/Campground_Search_API>
* Campground Details API: <https://developer.active.com/docs/read/Campground_Details_API>

A call to the _Campground Search API_ provides the following output:
```<result
  contractID="CO"
  contractType="STATE"
  facilityID="50032"
  facilityName="MUELLER STATE PARK"
  faciltyPhoto="/photos/details/co_50032_1.jpg"
  latitude="38.8947222"
  longitude="-105.1794444"
  sitesWithAmps="Y"
  sitesWithPetsAllowed="Y"
  sitesWithSewerHookup="N"
  sitesWithWaterHookup="N"
  sitesWithWaterfront=""
  state="CO"/>
  ```

The `siteType` parameter uses the following key (if unspecified, all site types are returned):

| Type            | Code  |
| ----------------|:-----:|
| RV Sites        |  2001 |
| Cabins/Lodgings | 10001 |
| Tent            |  2003 |
| Trailer         |  2002 |
| Group Site      |  9002 |
| Day Use         |  9001 |
| Horse Site      |  3001 |
| Boat Site       |  2004 |

This is particularly useful if we want to delineate viable road trips based on vehicle type, such as car/tent vs. RV, in this case only a subset of all parks or campsites would be supportive of electrical / water facilities.

A call to the _Campground Details API_ provides the following output:
```<detailDescription
  alert="BEAR ALERT: BLACK BEARS ARE COMMON IN THE PARK. FOOD STORAGE REGULATION
   STRICTLY ENFORCED! FIRST COME FIRST SERVE CAMPING MAY BE AVAILBLE OUTSIDE
   THE RESERVATION DATES. CONTACT THE PARK FOR INFORMATION."
  contractID="CO"
  description="The Mueller cabins are only reservable through the call center.      
   Mueller State Park is open year round. With its wealth of aspen trees, each
   season is a delight for photographers and sightseers visiting the park. Over
   fifty miles of scenic trails invite you to explore the park&amp;#39;s rare beauty.
   Hiking, camping, mountain biking, horseback riding, snow shoeing, cross country
   skiing and nature study are the park&amp;#39;s main attractions.  Mueller&amp;#39;s 5,121
   acres of aspen and conifer forests are home to an abundance of wildlife including
   black bear, elk, deer, fox, coyotes, &amp; hawks. 132 campsites in seven loops
   include 110 electrical sites accommodating motor homes, trailers and tents, and 22
   walk-in tent only sites. Campsites fees range from $16 - $20. After the middle of October,
   limited winter campsites are available first come/first serve. For more information,
   call the park at 719-687-2366."
  drivingDirection="25 miles west of Colorado Springs on Hwy 24 to Divide. Then 3 1/2
   miles south on Hwy 67 to the park entrance."
  facilitiesDescription=""
  facility="MUELLER STATE PARK"
  facilityID="50032"
  importantInformation=" ATTENTION TENT CAMPERS: When checking site information, tent
   campers must scroll down and read the &quot;IMPORTANT INFORMATION&quot; which will
   contain tent size information for that site. Some sites will not accommodate tents.
   ATTENTION ALL CAMPERS: Mueller is Black Bear country. Proper food storage is required
   per regulations. IMPORTANT RESERVATION INFORMATION: Mueller&amp;#39;s campsites are
   on reservations approximately the middle of May through the middle of October. Reservations
   must be made at least three days in advance of your arrival. Aspen Leaf Annual Pass holders
   can make discounted reservations online. In addition to the camping fee, a parks pass
   (annual or daily) is required on all vehicles entering the park. Parks passes are not
   included in reservation fees. FIRST-COME, FIRST-SERVE CAMPING MAY BE AVAILBLE OUTSIDE THE
   RESERVATION DATES. CONTACT THE PARK FOR INFORMATION. "
  latitude="38.8947222"
  longitude="-105.1794444"
  nearbyAttrctionDescription=""
  orientationDescription=""
  recreationDescription=""
  reservationUrl="http://www.reserveamerica.com/campsiteSearch.do?contractCode=CO&amp;parkId=50032">
  <address city="DIVIDE" country="United States" state="Colorado"
   streetAddress="P.O. BOX 39" zip="80814"/>
   ```

This not only provides latitude and longitude information but also a street address and postal code of the location. Moreover, the text provided could be used to populate a description of destinations along the trip. The _Campground Details API_ also provides photos (where available) of the location, via the [Reserve America](https://www.reserveamerica.com/) website.

Finally, the _Campground Details API_ also provides a list of amenities in each park or campground, in the following format:
```  <contact name="Direct Line" number="7196872366"/>
  <contact name="Ranger Station" number="7196872366"/>
  <amenity distance="Within Facility" name="Biking"/>
  <amenity distance="Within Facility" name="Bird Watching"/>
  <amenity distance="Within Facility" name="Camper Services Bldg"/>
  <amenity distance="Within Facility" name="Comfort Station"/>
  <amenity distance="Within Facility" name="Cross Country Skiing"/>
  <amenity distance="Within Facility" name="Dump Station"/>
  <amenity distance="Within Facility" name="Firewood Available"/>
  <amenity distance="Within Facility" name="Fishing"/>
  <amenity distance="Within Facility" name="Group Campground"/>
  <amenity distance="Within Facility" name="Hiking"/>
  <amenity distance="Within Facility" name="Horseback Riding"/>
  <amenity distance="Within Facility" name="Hunting"/>
  <amenity distance="Within Facility" name="Interpretitive Programs"/>
  <amenity distance="Within Facility" name="Laundry Facilities"/>
  <amenity distance="Within Facility" name="Natural Shade"/>
  <amenity distance="Within Facility" name="Nature Study Exhibits"/>
  <amenity distance="Within Facility" name="Parking"/>
  <amenity distance="Within Facility" name="Photography"/>
  <amenity distance="Within Facility" name="Picnic Tables"/>
  <amenity distance="Within Facility" name="Picnicking"/>
  <amenity distance="Within Facility" name="Playground"/>
  <amenity distance="Within Facility" name="Proximity To Camp Serv."/>
  <amenity distance="Within Facility" name="Ranger Station"/>
  <amenity distance="Within Facility" name="Showers"/>
  <amenity distance="Within Facility" name="Snow Shoeing"/>
  <amenity distance="Within Facility" name="Snow Sledding"/>
  <amenity distance="Within Facility" name="Visitor Center"/>
  <amenity distance="Within Facility" name="Wildlife Watching Opportunity"/>
  ```

The main potential disadvantage of working with the _ActiveAccess_ APIs is the data type. The current versions of the APIs provide output as `.XML` which may require more steps to clean and format than `JSON` APIs that are potentially more user-friendly.

* Park Availability

Campsite availability is a notorious thorn in the side of any camper, especially during the summer months. Parks that are fully occupied won't make a suitable destination for our would-be road trippers. Perhaps out of scope for our current project, but wanted to footnote it here. Various attempts have been made to programmatically scrape the various provincial parks reservations platforms for campsite availability, for example [here](https://www.cbc.ca/news/canada/british-columbia/savvy-coders-find-way-to-nab-coveted-b-c-camping-spots-1.6081267) or [here (closed source)](https://campnab.com/) or [here (closed source)](https://sitescout.ca/).


# Projects for reference
<https://github.com/rhiever/Data-Analysis-and-Machine-Learning-Projects/blob/master/pareto-optimized-road-trip/optimized-state-capitols-trip.ipynb>

# Flex Goals

## Preferences
* Explore additional training data and compare the accuracy.
* Input loop + retraining.
* Maybe, post-trip the user rates each attraction /5 and that is used to re-weight their own assigned "rating"
* Predicting ratings (can we replicate was was done by [Vasanth](https://vasanth16.github.io/#Part-6:-Predicting-Ratings) project?)

## Recommendations
* filter out/for place `type`(s)

## Itinerary
* multi-stop
* multi-day
* multi-route
* time (driving hours/distance per day, time to stop at each attraction - can the suggested trip be done in the allotted time?)
* time of day
For eg. not all attractions can be visited at all times. Can use `opening_hours`
```      "opening_hours":
        {
          "open_now": false,
          "periods":
            [
              {
                "close": { "day": 1, "time": "1700" },
                "open": { "day": 1, "time": "0900" },
              },
              {
                "close": { "day": 2, "time": "1700" },
                "open": { "day": 2, "time": "0900" },
              },
              {
                "close": { "day": 3, "time": "1700" },
                "open": { "day": 3, "time": "0900" },
              },
              {
                "close": { "day": 4, "time": "1700" },
                "open": { "day": 4, "time": "0900" },
              },
              {
                "close": { "day": 5, "time": "1700" },
                "open": { "day": 5, "time": "0900" },
              },
            ],
          "weekday_text":
            [
              "Monday: 9:00 AM – 5:00 PM",
              "Tuesday: 9:00 AM – 5:00 PM",
              "Wednesday: 9:00 AM – 5:00 PM",
              "Thursday: 9:00 AM – 5:00 PM",
              "Friday: 9:00 AM – 5:00 PM",
              "Saturday: Closed",
              "Sunday: Closed",
            ],
        },
```

* Budget
* filter by 
* gas costs? (vehicle type?)