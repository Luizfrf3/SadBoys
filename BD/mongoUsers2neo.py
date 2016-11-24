from pymongo import MongoClient
from py2neo import *

d = MongoClient().twitter.users
g = Graph(bolt = False, password = "neo4j")

cursor = d.find()

i = 1
# Insere todos os usuários primeiro
for user in cursor:
	s = user['id_str']
	query = "match (t:tweet) where t.user_id = '%s' return count(t) as n" % s
	c = g.run(query)
	if c['n'] > 0:
		fr = user['friends']
		fo = user['followers']
		userNode = Node(
			"user", 
			name = user['name'],
			id = user['id_str'],
			profile_image = user['profile_image_url'],
			friends = fr,
			followers = fo,
			label = 0.5
		)
		g.create(userNode)
		print i
		i += 1

query = "match (t:tweet), (u:user) where u.id = t.user_id create (u)-[:twitted]->(t)"

g.run(query)
