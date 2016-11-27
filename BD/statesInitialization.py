from py2neo import *
import csv

#g = Graph(password="123456")
g = Graph(bolt=False, password="neo4j")


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
						print(name+':'+field)
						print(l[field])
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

print ([state for state in states])

i = 1

for entry in states:
	state = states[entry]
	stateNode = Node(
		"state", 
		name = entry,
		position = state['Position'],
		rate = state['Rate'],
		episode_18_ = state['episode:18-'],
		episode_12_17 = state['episode:12-17'],
		episode_18_25 = state['episode:18-25'],
		episode_26_ = state['episode:26-'],
		tought_18_ = state['tought:18-'],
		tought_18_25 = state['tought:18-25'],
		tought_26_ = state['tought:26-'],
		avg_label = 0.5
	)
	g.create(stateNode)
	print (i)
	i += 1

query = """
match (t:tweet) 
match (s:state) 
where s.name = t.state 
create (s)-[:has]->(t)
"""
g.run(query)

query = """
match (s:state)-[:has]->(t:tweet)
with s, avg(t.label) as avg_l
set s.avg_label = avg_l
"""

g.run(query)










