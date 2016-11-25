import tw_dataset as db

banco = db.tw_dataset(10)

tweets = banco.get_next_batch()

print tweets
