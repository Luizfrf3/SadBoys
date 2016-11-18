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

cursor = c.find(query, limit=20)

for tweet in cursor:
	coordinates = tweet['coordinates']
	print coordinates
