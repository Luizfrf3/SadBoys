"""
    Cria os indices para todas as propriedades nos dois grafos

    Autores: Lucas Alves Racoci - RA 156331
             Luiz Fernando Rodrigues da Fonseca - RA 156475

"""

from py2neo import *

g = Graph(bolt = False, password = "neo4j")

g.schema.create_index("tweet", "text")
g.schema.create_index("tweet", "user_id")
g.schema.create_index("tweet", "coordinates")
g.schema.create_index("tweet", "created_at")
g.schema.create_index("tweet", "label")
g.schema.create_index("tweet", "state")

g.schema.create_index("user", "id")
g.schema.create_index("user", "name")
g.schema.create_index("user", "profile_image")
g.schema.create_index("user", "label")

g.schema.create_index("tweetglobal", "text")
g.schema.create_index("tweetglobal", "user_id")
g.schema.create_index("tweetglobal", "tweet_id")
g.schema.create_index("tweetglobal", "created_at")
g.schema.create_index("tweetglobal", "label")

g.schema.create_index("userglobal", "id")
g.schema.create_index("userglobal", "name")
g.schema.create_index("userglobal", "screen_name")
g.schema.create_index("userglobal", "profile_image")
g.schema.create_index("userglobal", "profile_image_https")
g.schema.create_index("userglobal", "label")
g.schema.create_index("userglobal", "description")

g.schema.create_index("state", "position")
g.schema.create_index("state", "rate")
g.schema.create_index("state", "episode_18_")
g.schema.create_index("state", "episode_12_17")
g.schema.create_index("state", "episode_18_25")
g.schema.create_index("state", "episode_26_")
g.schema.create_index("state", "tought_18_")
g.schema.create_index("state", "tought_18_25")
g.schema.create_index("state", "tought_26_")
g.schema.create_index("state", "avg_label")
