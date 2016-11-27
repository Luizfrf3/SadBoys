# Inicializa o banco com os dados dos filmes
from py2neo import *
import csv
#g = Graph(password="123")
#g = Graph(bolt=False, password="neo4j")


fName = {
	'rate': "suicide_rate_per_state", 
	'episode': "depressive_episode_per_state", 
	'tought': "suicide_toughts_per_state"
}

fPath = {name: "../suicide_depression/"+fName[name]+".csv" for name in fName}


states = {}


with open(fPath['rate']) as csvfile:
	reader = csv.DictReader(csvfile)
	for l in reader:
		states[l['State']] = {field: l[field] for field in l if field != 'State'}

for name in fPath:
	if(name != 'rate'):
		print(name)
		with open(fPath[name]) as csvfile:
			reader = csv.DictReader(csvfile)
			for l in reader:
				for field in l:
					if field != 'State':
						states[l['State']][name+':'+field] = l[field] 
	
print (states)

for state in states:
	for field in states[state]:
		if states[state][field][-1] == '%':
			states[state][field] = float(states[state][field][:-1])/100
		elif field != 'Position':
			states[state][field] = float(states[state][field])
		else:
			states[state][field] = int(states[state][field])
		print(field+": "+str(states[state][field]))

print (states)





