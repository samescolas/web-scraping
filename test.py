from database import Database
from sys import argv
import os

try:
	config = pickle.load(open("config.pickle", "rb"))
except:
	config = {
		'image_dir': './imgs',
		'data_dir': './data'
	}

db = Database(config['data_dir'], '')

data_files = os.listdir(config['data_dir'])
for f in data_files:
	db.load(f)
	if len(argv) > 1:
		if argv[1] in f:
			print(db._data[0])
	else:
		print("[{}] {}".format(len(db._data), f))
