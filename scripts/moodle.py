from my_io import Dataset
import json

dataset = Dataset('moodle')
print('somme', [sum(dataset.data[i][j] for i in range(dataset.nb_students)) for j in range(dataset.nb_questions)])

new = []
for line in dataset.data:
    new.append(line[1:])
"""with open('data/moodle2.json', 'w') as f:
    f.write(json.dumps({'student_data': new}))
"""