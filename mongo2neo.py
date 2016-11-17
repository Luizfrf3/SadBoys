import pymongo
from py2neo import *

m = pymongo.MongoClient()
c = m.twitter.tweets

conta = c.count({ 'lang': 'en', '$or': [ { 'geo': { '$ne':'null' } }, { 'place': { '$ne':'null' } }, { 'coordinates': { '$ne':'null' } } ] })

print conta 
