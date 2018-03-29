import time

class ErrorLog:

	def __init__(self, fp):
		self.fp = fp

	def write(self, err):
		fd = open(self.fp, 'a+')
		fd.write("[{}]\t{}\n".format(int(time.time()), str(err)))
		fd.close()
