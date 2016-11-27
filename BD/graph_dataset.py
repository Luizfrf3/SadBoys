"""
    Implementacao de API que se comunica com o modulo de visualizacao
    que mostrara o grafo dos usuarios e suas relacoes na tela

    Autores: Lucas Alves Racoci - RA 156331
             Luiz Fernando Rodrigues da Fonseca - RA 156475

"""

from py2neo import *
import numpy as np
from py2neo.packages.httpstream import http

class graph_dataset:
	# Inicializa o tempo do socket e o neo4j
	def __init__(self):

		http.socket_timeout = 9999
		self.g = Graph(bolt = False, password = "neo4j")

	# Dado o nome unico do usuario, retorna o id dele se existir
	def getUserID(self, screen_name):

		query = "match (u:userglobal) where u.screen_name = '%s' return u.id as id" % (screen_name)
		cursor = self.g.run(query)

		data = cursor.data()
		
		if data == None:
			return None

		return data[0]['id']

	# Retorna quem um usuario dado pelo id segue
	def getFollows(self, user_id):

		query = "match (u:userglobal) where u.id = '%s' return u" % (user_id)

		cursor = self.g.run(query)
		data = cursor.data()[0]['u']

		query = "match (u1:userglobal)-[:followsglobal]->(u2:userglobal) where u1.id = '%s' return u2.id as id, u2.label as label" % (user_id)

		cursor = self.g.run(query)
		followers = cursor.data()

		return data, followers
