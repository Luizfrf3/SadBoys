import pymongo
from py2neo import *

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

conta = c.find(query)

print conta 
