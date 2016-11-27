import pymongo

import pymongo
m = pymongo.MongoClient()
u = m.twitter.users
c = m.twitter.users
cursor = c.find(limit = 1000)

for u in cursor:
        print u
