from py2neo import *

g = Graph(password="123456")
#g = Graph(bolt=False, password="neo4j")

sentiment_labels = "stanfordSentimentTreebank/stanfordSentimentTreebank/sentiment_labels.txt" 
dictionary = "stanfordSentimentTreebank/stanfordSentimentTreebank/dictionary.txt"

f_sentiment = open(sentiment_labels)
sentiments = [line for line in f_sentiment]

f_dictionary = open(dictionary)
d = {}

for line in f_dictionary:
	s = line.split('|')
	d[int(s[1])] = s[0]

for i in range(1, 101):
	line = sentiments[i]
	x = tuple(line.split('\n')[0].split('|'))
	query = "create (:frases{id:%s, val:%s, frase:{f}})" % x
	g.run(query, f = d[int(x[0])])
