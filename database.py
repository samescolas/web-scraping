import pickle
from errorlog import ErrorLog

# Database is a file 
class Database:

	def __init__(self, data_dir, prefix):
		self.files_written = 0
		self._data = []
		self.data_dir = data_dir
		self.prefix = prefix
		self.error = ErrorLog('./error.log')

	def save(self, data):
		try:
			with open("{}/{}-{}.pickle".format(self.data_dir, self.prefix, self.files_written), 'wb') as fd:
				self.files_written += 1
				pickle.dump(data, fd, protocol=pickle.HIGHEST_PROTOCOL)
		except:
			self.error.write('Unable to open database.')

	def load(self, filepath):
		try:
			self._data = pickle.load( open("{}/{}".format(self.data_dir, filepath), 'rb') )
		except FileNotFoundError:
			self._data = []
