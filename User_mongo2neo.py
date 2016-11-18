import pymongo
from py2neo import *
from geopy import Nominatim
import time

g = Graph(bolt = False, password = "neo4j")
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

cursor = c.find(query, limit = 100)

geolocator = Nominatim(timeout = 5)

for tweet in cursor:
	place = tweet['place']
	coordinates = tweet['coordinates']
	location = None

	if coordinates != None:
		lon = coordinates['coordinates'][0]
		lat = coordinates['coordinates'][1]
		if -170 < lon < -60 and 12 < lat < 72:
			tries = 3
			while tries > 0:
				try:
					time.sleep(1)
					location = geolocator.reverse("%f, %f" % (lat, lon))
					break
				except geopy.exc.GeocoderTimedOut:
					time.sleep(1)
					tries -= 1
				except geopy.exc.QuotaExceeded:
					time.sleep(10)

	elif place != None:
		place_coordinates = place['bounding_box']['coordinates']
		lon = (float(place_coordinates[0][0][0]) + float(place_coordinates[0][1][0])) / 2
		lat = (float(place_coordinates[0][0][1]) + float(place_coordinates[0][2][1])) / 2
		if -170 < lon < -60 and 12 < lat < 72 and place['country'] == "United States":
			tries = 3
			while tries > 0:
				try:
					time.sleep(1)
					location = geolocator.reverse("%f, %f" % (lat, lon))
					break
				except geopy.exc.GeocoderTimedOut:
					time.sleep(1)
					tries -= 1
				except geopy.exc.QuotaExceeded:
					time.sleep(10)
	
	if location != None:
		tweet_node = """Node("tweet", text = "%s", user_id = %s, label = 0.5, coordinates = [%f, %f], state = "%s" """ % (tweet['text'], tweet['user']['id_str'],lat, lon, location.raw['address']['state'])
		print(tweet_node)
