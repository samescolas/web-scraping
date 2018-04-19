import scrapy
from scrapy.http import Request

cities = ['newyork', 'boston', 'seattle', 'sanfrancisco', 'austin', 'providence', 'chicago', 'detroit', 'denver']

class CLSpider(scrapy.Spider):
	name = 'house-spider'
	#start_urls = ['https://{}.craigslist.org/d/jobs/search/jjj'.format(city) for city in cities]
	start_urls = ['https://newyork.craigslist.org/search/hhh']

	def parse(self, response):
		for house in response.css('p.result-info'):
			post_dt = house.css('time.result-date::text').extract_first()
			title = house.css('a.result-title::text').extract_first()
			price = house.css('span.result-price::text').extract_first()
			info = house.css('span.housing::text').extract_first()
			link = house.css('a.result-title::attr(href)').extract_first()
			#yield Request(link, callback=self.parse_ad, meta={ 'title': title })
			yield Request(link, callback=self.parse_ad, meta={ 'link': link, 'post_dt': post_dt, 'title': title, 'price': price, 'info': info })

	def parse_ad(self, response):
		description = "".join(line for line in response.css('section#postingbody::text').extract())
		imgs = ",".join(img for img in response.css('a.thumb::attr(href)').extract())
		attrgrp1 = response.css('span.shared-line-bubble b::text').extract()
		attrgrp2 = response.css('p.attrgroup span::text').extract()
		bedrooms = None
		bathrooms = None
		sqft = None
		available = None
		dogs = None
		cats = None
		smoking = None
		factoids = []
		for thing in attrgrp1:
			thing = thing.lower()
			if 'br' in thing:
				bedrooms = float(thing.replace('br', ''))
			elif 'ba' in thing:
				bathrooms = float(thing.replace('ba', ''))
			else:
				sqft = float(thing)
		for thing in attrgrp2:
			thing = thing.lower()
			if 'available' in thing:
				available = thing
			elif 'smoking' in thing:
				if 'no' in thing:
					smoking = False
				elif 'ok' in thing:
					smoking = True
			elif 'dog' in thing and 'cat' in thing:
				if 'ok' in thing:
					dogs = True
					cats = True
				else:
					dogs = thing
					cats = thing
			elif 'dog'  in thing:
				if 'ok' in thing or 'friendly' in thing:
					dogs = True
				elif 'not' in thing or 'no' in thing:
					dogs = False
			elif 'cat'  in thing:
				if 'ok' in thing or 'friendly' in thing:
					cats = True
				elif 'not' in thing or 'no' in thing:
					cats = False
			elif 'pet' in thing:
				if 'ok' in thing or 'friendly' in thing:
					dogs = True
					cats = True
				elif 'not' in thing or 'no' in thing:
					dogs = False
					cats = False
			elif len(thing) > 2 and 'ft' not in thing:
				factoids.append(thing)

		yield {
			'description': description,
			'imgs': imgs,
			'title': response.meta.get('title'),
			'post_dt': response.meta.get('post_dt'),
			'price': response.meta.get('price'),
			'link': response.meta.get('link'),
			'info': response.meta.get('info'),
			'bedrooms': bedrooms,
			'bathrooms': bathrooms,
			'sqft': sqft,
			'available': available,
			'factoids': ",".join(factoids),
			'smoking': smoking,
			'dogs': dogs,
			'cats': cats
		}
