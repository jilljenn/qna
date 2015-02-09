import json

PREFIX = 'edm-castor'

def split(filename, n):
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

def backup(filename, data):
	with open('%s/%s.json' % (PREFIX, filename), 'w') as f:
		f.write(json.dumps(data))

def load(filename, prefix=PREFIX):
	return json.load(open('%s/%s.json' % (prefix, filename)))
