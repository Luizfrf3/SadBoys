from py2neo import *
import numpy as np
from py2neo.packages.httpstream import http

class graph_dataset:
	def __init__(self):

		http.socket_timeout = 9999
		self.g = Graph(bolt = False, password = "neo4j")

	def getUserID(self, screen_name):

		query = "match (u:userglobal) where u.screen_name = '%s' return u.id as id" % (screen_name)
		cursor = self.g.run(query)

		return cursor.data()[0]['id']

	def getFollowers(self, user_id):

		query = "match (u:userglobal) where u.id = '%s' return u" % (user_id)

		cursor = self.g.run(query)
		data = cursor.data()[0]['u']

		query = "match (u1:userglobal)-[:followsglobal]->(u2:userglobal) where u1.id = '%s' return u2.id as id, u2.label as label" % (user_id)

		cursor = self.g.run(query)
		followers = cursor.data()

		return data, followers
