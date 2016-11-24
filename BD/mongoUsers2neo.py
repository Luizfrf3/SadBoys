from pymongo import MongoClient
from py2neo import *

d = MongoClient().twitter.users
g = Graph(bolt = False, password = "neo4j")

cursor = d.find()

# Insere todos os usuários primeiro
for user in cursor:
	s = user['id_str']
	query = "match (t:tweet) where t.user_id = '%s' return count(t) as n" % s
	c = g.run(query)
	if c['n'] > 0:
		userNode = Node(
			"user", 
			name = user[u'name'],
			id = user[u'id_str'],
			friends = user[u'friends']
			followers = user[u'followers']
			label = 0.5
		)
		g.create(userNode)

query = "match (t:tweet), (u:user) where u.id = t.user_id create (u)-[:twitted]->(t)"

g.run(query)
