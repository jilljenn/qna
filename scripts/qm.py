import json

q = json.load(open('lastchance/qmatrix-26102014232558.json'))
data = json.load(open('data/castor6e.json'))['student_data']

print ' & '.join(['Q-Matrix', 'Guess', 'Slip', 'Correct\\\\'])
for i, line in enumerate(q['Q']):
    print int(line[0]), '&', int(line[1]), '&', int(line[2]), '&', round(q['guess'][i], 3), '&', round(q['slip'][i], 3), '&', round(sum(data[k][i] for k in range(48939)) / 48939. * 100), '\\\\'
