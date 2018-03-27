import multiprocessing as multi
import numpy as np
import random
import time
from scraper import BikeScraper
from database import Database
from proxy import Proxy
import pickle

try:
	config = pickle.load(open("config.pickle", "rb"))
except:
	config = {
		'image_dir': './imgs',
		'data_dir': './data'
	}

config['base_url'] = 'https://www.bike-parts-honda.com'

def perform_extraction(pages):
	for page in pages:
		p = Proxy()
		# Get a few random proxies (don't want to overload
		# proxy API (230 max requests) or send too many
		# from the same IP continuously
		proxies = [ p.get_proxy() for i in range(3) ]
		db = Database(config['data_dir'], 'united_kingdom')
		s = BikeScraper(proxies, 'united kingdom', config['base_url'], config['image_dir'], True, False)
		# start on page 1
		bikes = s.get_bikes(page)
		db.save(bikes)
		time.sleep(random.randint(1, 15))


cpus = multi.cpu_count()
workers = []

page_bins = np.array_split([i for i in range(1, 144)], cpus)

for cpu in range(cpus):
	print("Starting scraper on CPU {}.".format(cpu))
	worker = multi.Process(name=str(cpu),
						   target=perform_extraction,
						   args=(page_bins[cpu],))

	worker.start()
	workers.append(worker)

for worker in workers:
	worker.join()
