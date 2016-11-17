import tr_dataset as db

banco = db.tr_dataset(10)

for i in range(0, 10):
	input, labels = banco.get_next_batch()

print input
print labels