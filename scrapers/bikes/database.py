import pickle
from errorlog import ErrorLog

# Database is a file 
class Database:

	def __init__(self, data_dir, prefix):
		self._data = []
		self.data_dir = data_dir
		self.prefix = prefix
		self.error = ErrorLog('./error.log')

	def create_filename(self):
		return '{}/{}.pickle'.format(self.data_dir, self.prefix)

	def save(self, data):
		try:
			with open(self.create_filename(), 'wb') as fd:
				pickle.dump(data, fd, protocol=pickle.HIGHEST_PROTOCOL)
		except:
			self.error.write('Unable to open database.')

	def load(self, filepath):
		del self._data
		try:
			with open('{}/{}'.format(self.data_dir, filepath), 'rb') as fd:
				self._data = pickle.load(fd)
		except:
			self._data = []
		return True
