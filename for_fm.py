from my_io import Dataset
import random


dataset = Dataset('berkeley')
print(dataset.nb_students)
print(dataset.nb_questions)
#print(dataset.data)
with open('/tmp/train.dat', 'w') as train:
	with open('/tmp/test.dat', 'w') as test:
		for i in range(dataset.nb_students):
			for j in range(dataset.nb_questions):
				line = ','.join([str(i), str(j), '1' if dataset.data[i][j] else '0']) + '\n'
				if random.random() < 0.8:
					train.write(line)
				else:
					test.write(line)
