import heatmap_dataset as db

banco = db.heatmap_dataset()

data = banco.getStateData('New York')

print data

tweets = banco.getTweets()

print tweets[0:10]
