"""
    Implementacao de API que se comunica com o modulo de visualizacao
    que mostrara o mapa de calor na tela

    Autores: Lucas Alves Racoci - RA 156331
             Luiz Fernando Rodrigues da Fonseca - RA 156475

"""

from py2neo import *
import numpy as np
from py2neo.packages.httpstream import http

class heatmap_dataset:
	# Inicializa o tempo do socket e o neo4j
	def __init__(self):

		http.socket_timeout = 9999
		self.g = Graph(bolt = False, password = "neo4j")

	# Dado o nome do estado americano, retorna os seus dados
	# de suicidio, depressao e media de sentimento
	def getStateData(self, state):

		query = "match (s:state) where s.name = '%s' return s.avg_label as avg_l, s.rate as suicide_rate, s.episode_18_ as depressive_percentage, s.tought_18_ as suicide_percentage" % (state)
		cursor = self.g.run(query)

		return cursor.data()[0]

	# Retorna as coordenadas e o sentimento de todos os tweets
	def getTweets(self):

		query = "match (t:tweet) return t.coordinates as coor, t.label as label"
		cursor = self.g.run(query)

		tweets = []

		for t in cursor:
			tweets.append({'coordinates': np.float64(t['coor']), 'label': float(t['label'])})

		return tweets
