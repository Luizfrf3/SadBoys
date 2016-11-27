from py2neo import *

g = Graph(bolt = False, password = "neo4j")

query = """
match (u:user)-[:twitted]->(t:tweet)
with u, avg(t.label) as avg_label
set u.label = avg_label
"""

g.run(query)

query = """
match (ug:userglobal)-[:twittedglobal]->(tg:tweetglobal)
with ug, avg(tg.label) as avg_label
set ug.label = avg_label
"""

g.run(query)
