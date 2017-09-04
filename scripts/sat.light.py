import json, random

nb_questions_total = 40
nb_questions = 20
nb_students = 50

sat = open('data/sat.csv').read().splitlines()
student_data = []
subset = sorted(random.sample(range(nb_questions_total), nb_questions))
for line in sat[1:nb_students + 1]:
	answers = map(lambda x: x == '1', line.split(','))
	student_data.append([answers[i] for i in subset])
with open('data/sat.light.json', 'w') as f:
	f.write(json.dumps({'student_data': student_data, 'subset': subset}))
