"""
    Insere os tweets do segundo grafo que serao usados
    no grafo de usuarios, usando so tweets em ingles

    Autores: Lucas Alves Racoci - RA 156331
             Luiz Fernando Rodrigues da Fonseca - RA 156475

"""

import pymongo
from py2neo import *
from py2neo.packages.httpstream import http
http.socket_timeout = 9999

# Inicializa os clientes dos bancos neo4j e mongodb
g = Graph(bolt = False, password = "neo4j")
m = pymongo.MongoClient()
c = m.twitter.tweets

query = { 
	"lang": "en"
}

cursor = c.find(query, no_cursor_timeout = True)[0:1000000]

# Insere o tweet e suas informacoes necessarias
i = 1
for tweet in cursor:
	tweet_node = Node("tweetglobal", text = tweet['text'], user_id = tweet['user']['id_str'], label = 0.5, created_at = tweet['created_at'], tweet_id = tweet['id_str'])
	g.create(tweet_node)
	print i
	i += 1
