from my_io import Dataset

dataset = Dataset('berkeley')
print(dataset.nb_students)
print(dataset.nb_questions)
#print(dataset.data)
with open('/tmp/berkeley.dat', 'w') as f:
	for i in range(dataset.nb_students):
		for j in range(dataset.nb_questions):
			f.write('::'.join([str(i + 1), str(j + 1), '1' if dataset.data[i][j] else '0', '1']) + '\n')
