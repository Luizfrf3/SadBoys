from py2neo import *

g = Graph(password="123456")

sentiment_labels = "stanfordSentimentTreebank/stanfordSentimentTreebank/sentiment_labels.txt" 

file = open(sentiment_labels)
lines = [line for line in file]
for i in range(1,50):
	line = lines[i]
	x = tuple(line.split('\n')[0].split('|'))
	query = "create (:frases{id:%s, val:%s})" % x
	print(query)
	g.run(query)

datasetSentences = "stanfordSentimentTreebank/stanfordSentimentTreebank/datasetSentences.txt"

file = open(datasetSentences)
lines = [line for line in file]

for i in range(1,50):
	line = lines[i]
	[id,frase]= line.split('\n')[0].split('\t')
	query = "match (f:frases) where f.id = {id} set f.frase = {frase}"
	print(frase)
	print("\n")
	g.run(query, id = id, frase = frase)
