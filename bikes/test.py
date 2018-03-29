from database import Database
from sys import argv
from pprint import pprint
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
sorted_files = ['{}.pickle'.format(f) for f in sorted([int(s.split('.')[0]) for s in data_files])]
for f in sorted_files:
	db.load(f)
	if len(argv) > 1:
		if argv[1] in f:
			parts = db._data[0]['parts']
			bike = db._data[0]
			bike['parts'] = bike['parts'][0:2]
			bike['parts'][0]['part_data'] = bike['parts'][0]['part_data'][0:2]
			bike['parts'][1]['part_data'] = bike['parts'][1]['part_data'][0:3]
			pprint(bike)
	elif len(db._data) > 0:
		print("[{}] {}".format(len(db._data), f))
	else:
		print('[0] {}'.format(f))
