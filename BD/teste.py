import graph_dataset as db

banco = db.graph_dataset()

user_id = banco.getUserID('screen_name')

print user_id

data, followers = banco.getFollowers(user_id)

print data

print followers
