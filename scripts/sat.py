import json

sat = open('data/sat.csv').read().splitlines()
student_data = []
for line in sat[1:]:
	student_data.append(map(lambda x: x == '1', line.split(',')))
with open('data/sat.json', 'w') as f:
	f.write(json.dumps({'student_data': student_data}))
