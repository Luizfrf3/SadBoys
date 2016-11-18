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

cursor = c.find(query, limit=100)

geolocator = Nominatim()

cont = 0
for tweet in cursor:
	place = tweet['place']
	coordinates = tweet['coordinates']
	location = None
	if coordinates != None:
		coordinates = coordinates['coordinates']
		location = geolocator.reverse("%f, %f" % (coordinates[1], coordinates[0]))		
	flag = 0
	if location != None and place != None:
		country = place['country']
		if country == "United States":
			cont += 1
			flag = 1
	if location != None:
		country = location.raw['address']['country']
		if flag == 0 and country == "United States of America":
			cont += 1
			flag = 1
	if place != None:
		country = place ['country']
		if flag == 0 and country == "United States":
			cont += 1
print cont
