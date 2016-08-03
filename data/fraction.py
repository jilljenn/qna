import json

lines = open('fraction1.txt').read().splitlines()
lines2 = open('fraction2.txt').read().splitlines()
student_data = []
for i in range(len(lines)):
    first = list(map(lambda x: x == '1', lines[i].split()[1:]))
    second = list(map(lambda x: x == '1', lines2[i].split()[1:]))
    student_data.append(first + second)
with open('fraction.json', 'w') as f:
    f.write(json.dumps({'student_data': student_data}))
