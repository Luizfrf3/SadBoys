"""
    Extrai do mongodb os tweets que estao nos Estados Unidos, fazendo uso
    da API geopy.Nominatim para enviar as coordenadas geograficas do tweet
    e ela retornar o estado americano onde o tweet foi postado, e depois
    insere o tweet e todas as informacoes relevantes no grafo

    Autores: Lucas Alves Racoci - RA 156331
             Luiz Fernando Rodrigues da Fonseca - RA 156475

"""

import pymongo
from py2neo import *
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded, GeocoderUnavailable
import time
from py2neo.packages.httpstream import http
http.socket_timeout = 9999

# Inicializa os clientes e busca os tweets que tem algum tipo
# de localizacao geografica no mongodb
g = Graph(bolt = False, password = "neo4j")
m = pymongo.MongoClient()
c = m.twitter.tweets

query = { 
	"lang": "en", 
	"$or": [ 
		{ "place": { "$ne":None } }, 
		{ "coordinates": { "$ne":None } }, 
		{ "geo": { "$ne":None } }
	] 
}

cursor = c.find(query, no_cursor_timeout = True)

geolocator = Nominatim(timeout = 5)

# Offset para retomar execucao apos uma falha
offset = 0

# Para cada tweet encontrado, checa se ele esta dentro de um quadrado
# que engloba os Estados Unidos e chama o geolocator para conseguir
# as informacoes dos locais do tweet, sendo que e necessario dormir
# durante um segundo para nao exceder a quota da API
i = 1
for tweet in cursor:
	if i > offset:
		place = tweet['place']
		coordinates = tweet['coordinates']
		location = None

		if coordinates != None:
			lon = coordinates['coordinates'][0]
			lat = coordinates['coordinates'][1]
			if -170 < lon < -60 and 12 < lat < 72:
				tries = 3
				while tries > 0:
					try:
						time.sleep(1)
						location = geolocator.reverse("%f, %f" % (lat, lon))
						break
					except GeocoderTimedOut as e:
						print "GeocoderTimedOut"
						time.sleep(1)
						tries -= 1
					except GeocoderQuotaExceeded as e:
						print "QuotaExceeded"
						time.sleep(10)
					except GeocoderUnavailable as e:
						print "GeocoderUnavailable"
						time.sleep(30)

		elif place != None:
			if 'bounding_box' in place.keys() and place['bounding_box'] != None and 'coordinates' in place['bounding_box'].keys():
				place_coordinates = place['bounding_box']['coordinates']
				lon = (float(place_coordinates[0][0][0]) + float(place_coordinates[0][1][0])) / 2
				lat = (float(place_coordinates[0][0][1]) + float(place_coordinates[0][2][1])) / 2
				if -170 < lon < -60 and 12 < lat < 72 and place['country'] == "United States":
					tries = 3
					while tries > 0:
						try:
							time.sleep(1)
							location = geolocator.reverse("%f, %f" % (lat, lon))
							break
						except GeocoderTimedOut as e:
							print "GeocoderTimedOut"
							time.sleep(1)
							tries -= 1
						except GeocoderQuotaExceeded as e:
							print "QuotaExceeded"
							time.sleep(10)
						except GeocoderUnavailable as e:
							print "GeocoderUnavailable"
							time.sleep(30)

		# Se o tweet esta nos Estados Unidos e tem informacoes
		# do estado americano, insere o tweet no neo4j
		if location != None:
			if 'address' in location.raw.keys() and 'state' in location.raw['address'].keys() and 'country' in location.raw['address'].keys():
				if location.raw['address']['country'] == "United States of America":
					tweet_node = Node("tweet", text = tweet['text'], user_id = tweet['user']['id_str'], label = 0.5, coordinates = [lat, lon], state = location.raw['address']['state'], created_at = tweet['created_at'])
					g.create(tweet_node)
			else:
				print "Erro address/state"
	print i
	i += 1
