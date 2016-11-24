from pymongo import MongoClient
from py2neo import *

#d = MongoClient().twitter.users
g = Graph(password = "123456")
#g = Graph(bolt = False, password = "neo4j")

g.create(Node("tweet", user_id = '1'))
g.create(Node("tweet", user_id = '2'))
g.create(Node("tweet", user_id = '2'))
g.create(Node("tweet", user_id = '4'))

query = "match (t:tweet) return collect(distinct t.user_id) as ids"

idlist = g.run(query).next()['ids']
idset = set(str(x) for x in idlist)

#query = {
#	'id_str': { '$in': idlist }
#}

#cursor = d.find(query)
cursor = [
	{'name':'Zanoni', 'id_str':'1', 'profile_image_url':'xxx', 'followers':[{'id':2}]},
	{'name':'Gabriel', 'id_str':'2', 'profile_image_url':'xxx', 'followers':[]}
]

i = 1
for user in cursor:
	userNode = Node(
		"user", 
		name = user['name'],
		id = user['id_str'],
		profile_image = user['profile_image_url'],
		label = 0.5
	)
	g.create(userNode)
	print i
	i += 1

query = "match (t:tweet) match (u:user) where u.id = t.user_id create (u)-[:twitted]->(t)"

g.run(query)

#query = {
#	'id_str': { '$in': idlist }
#}

#cursor = d.find(query)

for user in cursor:
	g.run("match (u1:user) match (u2:user) where u1.id = {uid} and u2.id in {followers} create (u2)-[:follows]->(u1)", uid = user['id_str'], followers = [str(x['id']) for x in user['followers']])
