import tw_dataset as db

banco = db.tw_dataset(4)

tweets = banco.get_next_batch()

print tweets

tweets = banco.get_next_batch()

print tweets
