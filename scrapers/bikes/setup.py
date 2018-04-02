import sys
import os
import pickle

def prompt(q):
	return input("{}\n>> ".format(q))

try:
	config = pickle.load( open("config.pickle", 'rb') )
except:
	config = {
		'image_dir': '',
		'data_dir': ''
	}


image_dir = prompt('Where would you like the images saved?')
while not os.path.isdir(image_dir):
	yes = prompt("Directory {} does not exist. Would you like to create it now? [Y/N]".format(image_dir))
	if yes == 'Y' or yes == 'y':
		os.mkdir("./{}".format(image_dir))
		break
	else:
		image_dir = prompt('Where would you like the images saved? Please indicate a directory.')
print('Thank you.')
config['image_dir'] = image_dir

data_dir = prompt('Where would you like the data saved?')
while not os.path.isdir(data_dir):
	yes = prompt("Directory {} does not exist. Would you like to create it now? [Y/N]".format(data_dir))
	if yes == 'Y' or yes == 'y':
		os.mkdir("./{}".format(data_dir))
		break
	else:
		data_dir = prompt('Where would you like the data saved? Please indicate a directory.')
print('Thank you.')
config['data_dir'] = data_dir

with open("config.pickle", 'wb') as fd:
	pickle.dump(config, fd, protocol=pickle.HIGHEST_PROTOCOL)
