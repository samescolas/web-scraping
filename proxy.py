import requests
import json

class Proxy:
	def __init__(self):
		self.ip = ''
		self.port = ''
		self.api_requests = 0

	def get_proxy(self):
		# gimmeproxy rate limits @ 230 requests
		if self.api_requests > 200:
			return False
		try:
			self.api_requests += 1
			response = requests.get('https://gimmeproxy.com/api/getProxy')
			data = response.json()
			self.ip = data['ip']
			self.port = data['port']
		except:
			self.ip = '0'
			self.port = '80'
			return False
		return "http://{}".format(data['ipPort'])
