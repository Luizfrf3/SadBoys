import tw_dataset as db

banco = db.tw_dataset(4)

tweets = banco.get_next_batch()

banco.update([0,0,0,0])
