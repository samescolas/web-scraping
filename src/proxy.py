import requests
import json

class Proxy:
	def __init__(self):
		self.ip = ''
		self.port = ''
		self.api_requests = 0
		self.resources = [
			{
				'API': 'http://pubproxy.com/api/proxy',
				'limit': 100
			},
			{
				'API': 'https://gimmeproxy.com/api/getProxy',
				'limit': 230
			}
		]
		self.resource_ix = 0

	def get_proxy(self):
		# gimmeproxy rate limits @ 230 requests
		if self.api_requests > self.resources[self.resource_ix]['limit']:
			if self.resource_ix < len(self.resources):
				self.resource_ix += 1
				self.api_requests = 0
			else:
				return False
		try:
			self.api_requests += 1
			response = requests.get(self.resources[self.resource_ix]['API'])
			data = response.json()
			if self.resource_ix == 0:
				data = data['data'][0]
			self.ip = data['ip']
			self.port = data['port']
		except:
			return False
		return "http://{}".format(data['ipPort'])
