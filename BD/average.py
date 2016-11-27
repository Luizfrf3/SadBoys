"""
    Calcula as medias dos usuarios para os dois grafos,
    considerando os sentimentos dos seus tweets

    Autores: Lucas Alves Racoci - RA 156331
             Luiz Fernando Rodrigues da Fonseca - RA 156475

"""

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
