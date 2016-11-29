"""
    Insere os usuarios no grafo do grafo, criando as
    relacoes de twittar um tweet e seguir outro usuario

    Autores: Lucas Alves Racoci - RA 156331
             Luiz Fernando Rodrigues da Fonseca - RA 156475

"""

from pymongo import MongoClient
from py2neo import *

# Inicializa os clientes do banco
d = MongoClient().twitter.users

#g = Graph(password = "123456")
g = Graph(bolt = False, password = "neo4j")

# Busca no grafo os ids dos usuarios que postaram algum tweet do grafo
query = "match (t:tweetglobal) return collect(distinct t.user_id) as ids"

idlist = g.run(query).next()['ids']

query = {
	'id_str': { '$in': idlist }
}

cursor = d.find(query)

# Insere os usuarios que postaram tweets no grafo
i = 1
for user in cursor:
	userNode = Node(
		"userglobal", 
		name = user['name'],
		screen_name = user['screen_name'],
		id = user['id_str'],
		profile_image = user['profile_image_url'],
		profile_image_https = user['profile_image_url_https'],
		label = 0.5,
		description = user['description']
	)
	g.create(userNode)
	print i
	i += 1

# Cria as relacoes de twittar entre usuarios e tweets
query = "match (t:tweetglobal) match (u:userglobal) where u.id = t.user_id create (u)-[:twittedglobal]->(t)"

g.run(query)

# Cria as relacoes de um usuario seguir outro
query = {
	'id_str': { '$in': idlist }
}

cursor = d.find(query)

for user in cursor:
	if 'followers' in user.keys() and user['followers'] != None:
		g.run("match (u1:userglobal) match (u2:userglobal) where u1.id = {uid} and u2.id in {followers} create (u2)-[:followsglobal]->(u1)", uid = user['id_str'], followers = [str(x['id']) for x in user['followers']])
