import pymongo
from py2neo import *

m = pymongo.MongoClient()
c = m.twitter.tweets

query = { 
	'lang': 'en', 
	'$or': [ 
		{ 'geo': { '$ne': 'null' } }, 
		{ 'place': { '$ne':'null' } }, 
		{ 'coordinates': { '$ne':'null' } }
	]
}

conta = c.find(query).count()

print conta 
