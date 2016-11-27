from py2neo import *
import numpy as np
from py2neo.packages.httpstream import http

class heatmap_dataset:
	def __init__(self):

		http.socket_timeout = 9999
		self.g = Graph(bolt = False, password = "neo4j")

	def getStateData(self, state):

		query = ""
		cursor = self.g.run(query)

	def getTweets(self):

		query = "match (t:tweet) return t.coordinates as coor, t.label as label"
		cursor = self.g.run(query)

		tweets = []

		for t in cursor:
			tweets.append({'coordinates': np.float64(t['coor']), 'label': float(t['label'])})

		return tweets