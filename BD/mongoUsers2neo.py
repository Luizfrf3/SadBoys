from pymongo import MongoClient
from py2neo import *

d = MongoClient().twitter.users
g = Graph(bolt = False, password = "neo4j")

cursor = c.find()

# Insere todos os usuários primeiro
for user in cursor:
	userNode = Node(
		"user", 
		name = user[u'name'],
		id = user[u'id_str'],
		profile_image = user[u'profile_image_url']
	)
	g.create(userNode)

query = "MATCH (t:tweet) MATCH (u:user) WHERE u.id = t.user_id CREATE (u)-[:make]->(t);"

g.run(query) # Acho que é assim

# Agora, se ainda for necessário, deleta os nós que não ligaram com ninguém, mas isso parece muito arriscado








