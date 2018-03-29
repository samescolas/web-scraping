# used to parse HTML
from bs4 import BeautifulSoup

# used to request web pages
import requests

# impersonate a computer/phone
from user_agent import generate_user_agent

# regex library
import re

# used to copy image file objects to disk
import shutil

# generate timestamps
import datetime

# error logging
from errorlog import ErrorLog

# change proxies every so often
from proxy import Proxy

from random import randint

class BikeScraper:

	def __init__(self, proxy_list, country, base_url, imagepath, verbose=False, demo_mode=False):
		self.country = country
		self.verbose = verbose
		self.base_url = base_url
		self.imagepath = imagepath
		self.proxy = Proxy()
		self.proxies = { 'http': proxy_list[0] }
		self.proxy_list= proxy_list
		self.demo_mode = demo_mode
		self.error = ErrorLog('./error.log')
	

	def save_image(self, name, image_link):
		file_name = "{}/{}-{}.jpg".format(self.imagepath, re.sub('[^A-z\s]*', '', name).replace(' ', '_'), str(datetime.datetime.now().timestamp()).split('.')[0])
		if self.verbose:
			print("Saving image {}...".format(file_name))
		try:
			response = requests.get("{}/{}".format(self.base_url, image_link), proxies=self.proxies, stream=True)
		except:
			self.error.write("Unable to download image {}.".format(image_link))

		try:
			with open(file_name, 'wb') as fd:
				shutil.copyfileobj(response.raw, fd)
			del response
		except:
			self.error.write("Unable to save image {}.".format(image_link))
		return file_name

	def get_page(self, page_link, attempts=0):
		headers = { 'User-Agent': generate_user_agent(device_type='desktop', os=('mac', 'linux')) }
		if self.verbose:
			print("[{}] GET {}".format(self.proxies['http'], page_link))
		try:
			page_response = requests.get(page_link, timeout=5, headers=headers, proxies=self.proxies )
		except:
			if attempts < 3:
				return self.get_page(page_link, attempts+1)
			self.error.write("Error requesting page {}.".format(page_link))
			return False
		return BeautifulSoup(page_response.content, "html.parser")

	def switch_proxy(self, attempts=0):
		# 2% of the time when we call switch_proxy we will
		# spawn a new proxy to add to the list
		# this will help control the number of API requests to
		# the free proxy API
		if randint(1, 50) == 7 or attempts > 0:
			print('Getting a new proxy.')
			try:
				p = self.proxy.get_proxy()
				if not p:
					self.proxies = None
				self.proxy_list.append(self.proxy.get_proxy())
			except:
				if attempts > 3:
					return False
				return switch_proxy(attempts + 1)
		self.proxies = { 'http': self.proxy_list[randint(0, len(self.proxy_list) - 1)] }
		if self.verbose and self.proxies['http'] != False:
			print("Switched proxy to {}.".format(self.proxies['http']))
			

	def get_bikes(self, page):
		def scrape_bike_list(country, page):
			bikes = []

			page_content = self.get_page("https://www.bike-parts-honda.com/photo_moto-pieces---{}-{}.html".format(country.replace(' ', '+'), (page-1) * 30))
			if page_content == False:
				return []

			image_data = page_content.find_all(class_='openmodalbox')
			images = [img.find_all('img') for img in image_data]
			image_links = [i[1]['src'] for i in images]

			data = page_content.find_all('table')[5:(len(image_links)+5)]
			bike_links = [d.find_all('a') for d in data]
			for ix,bl in enumerate(bike_links):
				# If there is a parts catalog
				try:
					if len(bl) == 2:
						m = re.search('.*identification-(.*?).html', bl[0]['href'])
						model = m.group(1).strip()
						bikes.append({
							'model': model,
							'image': image_links[ix].strip(),
							'page': bl[0]['href'].strip()
						})
				except:
					continue
			
			return bikes

		def scrape_bike_page(bike, bike_page):
			attrs = bike_page.find_all(class_='ident_div_1')
			data = bike_page.find_all(class_='Texte_arial_bold_12_noir')
			vals = bike_page.find_all(class_='titre_12_red')
			cols = bike_page.find_all(class_='openmodalbox')

			# colors
			color_links = [c.find('img')['src'] for c in cols]
			c_ix = 0
			colors = []
			# metadata near top of page
			for i,d in enumerate(data):
				if i < len(vals):
					bike[d.text.strip(':').strip()] = vals[i].text.strip()
				# colors
				elif c_ix < len(color_links):
					colors.append({'id': d.text.strip(), 'image': color_links[c_ix]})
					c_ix += 1
			bike['color_data'] = colors
					
			# List of attributes (spark plug, etc.)
			for attr in attrs:
				try:
					a = attr.find('b').text.strip(':').strip()
					v = attr.find('img')
					va = attr.find_all('a')
					if len(va) > 0:
						v = va[0].text.strip()
					elif ':' in v.text:
						v = v.text.split(':')[1].strip()
					bike[a] = v
				except:
					continue

		def scrape_parts_page(bike_page, demo_mode):
			def get_part_data(part, link):
				parts = []
				page_content = self.get_page("{}/{}".format(self.base_url, link))
				img_link = page_content.find(class_='axzoomer')['src-big']
				part['imageLink'] = img_link
				part['imagePath'] = self.save_image(part['title'], img_link)
				# they've got some barriers in the way so we have to navigate a bit here..
				table_start_ix = str(page_content).find('verifidentification_v2_new_table')
				bs = BeautifulSoup(str(page_content)[table_start_ix:], "html.parser")
				td = bs.find_all('td')
				ix = 0
				while ix < len(td) - 5:
					try:
						parts.append({
							'num': td[ix].text,
							'name': td[ix+1].text,
							'part_number': td[ix+2].text,
							'price': td[ix+3].text,
							'quantity': td[ix+4].find('input')['value']
						})
					except:
						ix += 7
						continue
					ix += 7
				part['part_data'] = parts
			parts = []
			text = bike_page.find_all(class_='text_200')
			img = bike_page.find_all(class_='img_200')
			# for each part
			for i,t in enumerate(text):
				# only look at one part for testing
				if demo_mode and i == 2:
					break
				try:
					link = t.find('a')['href'].strip()
					part = {
						'link': link,
						'title': t.text.strip()
					}
					get_part_data(part, link)
					parts.append(part)
				except:
					continue
			return parts

		bikes = scrape_bike_list(self.country, page)
		if len(bikes) == 0:
			return False
		i = 0
		for bike in bikes:
			self.switch_proxy()
			bike_page = self.get_page("{}/{}".format(self.base_url, bike['page']))
			if self.verbose:
				print("Mining bike {}/30 from page {}...".format(i, bike['page']))
			if self.demo_mode and i == 2:
				break
			i += 1
			scrape_bike_page(bike, bike_page)
			bike['parts'] = scrape_parts_page(bike_page, self.demo_mode)
		return bikes
