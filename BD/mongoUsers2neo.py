"""
    Insere os usuarios no grafo do mapa de calor, criando as
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
query = "match (t:tweet) return collect(distinct t.user_id) as ids"

idlist = g.run(query).next()['ids']

query = {
	'id_str': { '$in': idlist }
}

cursor = d.find(query)

# Insere os usuarios que postaram tweets no grafo
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

# Cria as relacoes de twittar entre usuarios e tweets
query = "match (t:tweet) match (u:user) where u.id = t.user_id create (u)-[:twitted]->(t)"

g.run(query)

# Cria as relacoes de um usuario seguir outro
query = {
	'id_str': { '$in': idlist }
}

cursor = d.find(query)

for user in cursor:
	g.run("match (u1:user) match (u2:user) where u1.id = {uid} and u2.id in {followers} create (u2)-[:follows]->(u1)", uid = user['id_str'], followers = [str(x['id']) for x in user['followers']])
