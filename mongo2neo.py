import pymongo
from py2neo import *

m = pymongo.MongoClient()
c = m.twitter.tweets

conta = c.find({ "lang": "en", "$or": [ { "place": { "$ne":None } }, { "coordinates": { "$ne":None } }, { "geo": { "$ne":None } } ] })

print conta 
