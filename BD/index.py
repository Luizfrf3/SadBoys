from py2neo import *

g = Graph(bolt = False, password = "neo4j")

g.schema.drop_indexes("tweet")
g.schema.drop_indexes("user")
g.schema.drop_indexes("tweetglobal")

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
