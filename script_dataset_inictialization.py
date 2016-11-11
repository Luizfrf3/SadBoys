from py2neo import *

g = Graph(password="123456")

sentiment_labels = "/home/racoci/Documents/6Sem/BD/Datasets/stanfordSentimentTreebank/stanfordSentimentTreebank/sentiment_labels.txt" 

file = open(sentiment_labels)
lines = [line for line in file]
for i in range(1,50):
	line = lines[i]
	x = tuple(line.split('\n')[0].split('|'))
	query = "create (:frases{id:%s, val:%s})" % x
	print(query)
	g.run(query)

datasetSentences = "/home/racoci/Documents/6Sem/BD/Datasets/stanfordSentimentTreebank/stanfordSentimentTreebank/datasetSentences.txt"

file = open(datasetSentences)
lines = [line for line in file]

for i in range(1,50):
	line = lines[i]
	[id,val]= line.split('\n')[0].split('\t')
	query = "match (f:frases) where f.id = {id} set f.frase = {val}"
	print(val)
	print("\n")
	g.run(query, id = id, val = val)



