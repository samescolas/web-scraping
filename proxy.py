import requests
import json

class Proxy:
	def __init__(self):
		self.ip = ''
		self.port = ''

	def get_proxy(self):
		try:
			response = requests.get('https://gimmeproxy.com/api/getProxy')
			data = response.json()
			self.ip = data['ip']
			self.port = data['port']
		except:
			self.ip = '0'
			self.port = '80'
			return False
		return "http://{}".format(data['ipPort'])
