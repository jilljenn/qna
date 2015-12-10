import json
import os

PREFIX = 'japan'

class IO(object):
	def __init__(self):
		self.prefix = PREFIX + '0'
		for i in range(0, 5):
			self.update(i)
			if not os.path.exists(self.prefix):
				os.system('mkdir %s' % self.prefix)
		self.update(0)
		filename = '%s/%s' % (self.prefix, 'qmatrix-cdm.json')
		if not os.path.exists(filename):
			os.system('cp qmatrix-cdm.json %s' % filename)

	def update(self, step):
		prefix = list(self.prefix)
		prefix[-1] = str(step)
		self.prefix = ''.join(prefix)
		print('prefix is now', self.prefix)

	def split(self, filename, n):
		"""Creates files and returns filenames."""
		dataset = load(filename)['student_data']
		chunk_length = (len(dataset) - len(dataset) % n) / n
		bundle = []
		for k in range(n):
			train, test = [], []
			for i, line in enumerate(dataset):
				if k * chunk_length <= i < (k + 1) * chunk_length:
					test.append(line)
				else:
					train.append(line)
			bundle.append((train, test))
		return bundle

	def backup(self, filename, data):
		with open('%s/%s.json' % (self.prefix, filename), 'w') as f:
			f.write(json.dumps(data))

	def load(self, filename, prefix=None):
		if not prefix:
			prefix = self.prefix
		return json.load(open('%s/%s.json' % (prefix, filename)))
