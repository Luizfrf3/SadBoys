import pymongo
from py2neo import *
from geopy import Nominatim

m = pymongo.MongoClient()
c = m.twitter.tweets

query = { 
	"lang": "en", 
	"$or": [ 
		{ "place": { "$ne":None } }, 
		{ "coordinates": { "$ne":None } }, 
		{ "geo": { "$ne":None } }
	] 
}

cursor = c.find(query, limit=1000)

geolocator = Nominatim(timeout=5)

for tweet in cursor:
	place = tweet['place']
	coordinates = tweet['coordinates']
	location = None

	if coordinates != None:
		long = coordinates['coordinates'][0]
		lat = coordinates['coordinates'][1]
		if -170 < long < -60 and 12 < lat < 72:
			location = geolocator.reverse("%f, %f" % (lat, long), timeout = None)
			if location.raw['address']['country'] == "United States of America":
				print location.raw['address']['state']
	
	elif place != None:
		place_coordinates = place['bounding_box']['coordinates']
		long = (float(place_coordinates[0][0][0]) + float(place_coordinates[0][1][0])) / 2
		lat = (float(place_coordinates[0][0][1]) + float(place_coordinates[0][2][1])) / 2
		if -170 < long < -60 and 12 < lat < 72 and place['country'] == "United States":
                	location = geolocator.reverse("%f, %f" % (lat, long), timeout = None)
			print location.raw['address']['state']
