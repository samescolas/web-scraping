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

def perform_extraction(countries):
	for country in countries:
		p = Proxy()
		# Get a few random proxies (don't want to overload
		# proxy API (230 max requests) or send too many
		# from the same IP continuously
		proxies = [ p.get_proxy() for i in range(3) ]
		db = Database(config['data_dir'], country.replace(' ', '_'))
		s = BikeScraper(proxies, country, config['base_url'], config['image_dir'], True, True)
		# start on page 1
		page = 1
		bikes = s.get_bikes(page)
		while bikes:
			db.save(bikes)
			page += 1
			time.sleep(random.randint(1, 15))
			bikes = s.get_bikes(page)


# Generate list of countries from pulled list
with open('./countries.txt') as fd:
	countries = [c.strip() for c in fd.readlines()]

cpus = multi.cpu_count()
workers = []

page_bins = np.array_split(countries, cpus)

for cpu in range(cpus):
	print("Starting scraper on CPU {}.".format(cpu))
	worker = multi.Process(name=str(cpu),
						   target=perform_extraction,
						   args=(page_bins[cpu],))

	worker.start()
	workers.append(worker)

for worker in workers:
	worker.join()
