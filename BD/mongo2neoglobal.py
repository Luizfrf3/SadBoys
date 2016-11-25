import pymongo
from py2neo import *
from py2neo.packages.httpstream import http
http.socket_timeout = 9999

g = Graph(bolt = False, password = "neo4j")
m = pymongo.MongoClient()
c = m.twitter.tweets

query = { 
	"lang": "en"
}

cursor = c.find(query, no_cursor_timeout = True)

i = 1
for tweet in cursor:
	tweet_node = Node("tweetglobal", text = tweet['text'], user_id = tweet['user']['id_str'], label = 0.5, created_at = tweet['created_at'], tweet_id = tweet['id_str'])
	print i
	i += 1
