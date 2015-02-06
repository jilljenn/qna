# coding=utf8
import sys, os, re, json
import matplotlib.pyplot as plt

"""
loglosses_ltm = json.load(open('data/logloss-ltm.json'))
loglosses_qmatrix = json.load(open('data/logloss-qmatrix.json'))

fig, ax = plt.subplots()
ax.plot(range(len(loglosses_ltm)), loglosses_ltm, color='blue')
ax.plot(range(len(loglosses_qmatrix)), loglosses_qmatrix, color='red')
ax.set_title('Log loss')
plt.show()
"""

dataset = 'sat'
nb_competences = range(1, 30, 5)
if dataset == 'sat':
	train_power = '216'
elif dataset == 'castor6e':
	train_power = '48939'
else:
	train_power = '90'

graphs = {'20': {}, '40': {}, '80': {}, '90': {}, '160': {}, '216': {}, '276': {}, '286': {}, '295': {}, '48939': {}, '99': {}}
graphs2 = {10: {}, 15: {}, 20: {}, 30: {}, 40: {}, 17: {}, 3: {}}
filenames = {}

folder = sys.argv[1]

for filename in os.listdir(folder):
	if filename.startswith('stats'):
		print filename
		name, nb_questions, train_power = re.match('stats-%s-([a-z0-9-]+)-([0-9]+)-([0-9]+)-' % dataset, filename).groups()
		nb_questions = int(nb_questions)
		data = json.load(open('%s/%s' % (folder, filename)))['QMatrix' if len(name) <= 2 else 'IRT']['mean']
		# print name, nb_questions, train_power
		value = data[nb_questions / 2 - 1]
		if name not in graphs[train_power]:
			graphs[train_power][name] = {nb_questions: value}
		else:
			graphs[train_power][name][nb_questions] = value
		if name not in graphs2[nb_questions]:
			graphs2[nb_questions][name] = {train_power: value}
		else:
			graphs2[nb_questions][name][train_power] = value
		#if nb_questions == 17: # TODO mettre ça à 40
		filenames[(name, train_power)] = '%s/%s' % (folder, filename)

colors = {'3': 'red', '4': 'orangered', '5': 'orange', '6': 'yellow', 'irt': 'blue', 'mepv-irt': 'darkblue'}

"""
for train_power in ['40', '80', '160']:
	fig, ax = plt.subplots()
	for name in graphs[train_power]:
		x, y = [], []
		for i in [10, 15, 20, 30, 40]:
			if i in graphs[train_power][name]:
				x.append(i)
				y.append(graphs[train_power][name][i])
		ax.plot(x, y, color=colors[name])
	ax.set_title('train_power : %s' % train_power)
	plt.show()

for nb_questions in [10, 15, 20, 30, 40]:
	fig, ax = plt.subplots()
	for name in graphs2[nb_questions]:
		x, y = [], []
		for i in ['40', '80', '160']:
			if i in graphs2[nb_questions][name]:
				x.append(i)
				y.append(graphs2[nb_questions][name][i])
		ax.plot(x, y, color=colors[name])
	ax.set_title('nb_questions : %d' % nb_questions)
	plt.show()
"""

bundle = {}
bundle['nbq-17'] = graphs2[17]
# bundle['nbq-40'] = graphs2[40]

print filenames

#for train_power in ['48939']: # , '160'
print train_power
fig, ax = plt.subplots()
irt = json.load(open(filenames[('irt', train_power)]))['IRT']['mean']
# mepv_irt = json.load(open(filenames[('mepv-irt', train_power)]))['IRT']['mean']
bundle['irt-%s' % train_power] = irt
qmatrix = {}
for i, k in enumerate(nb_competences):
	qmatrix[k] = json.load(open(filenames[(str(k), train_power)]))['QMatrix']['mean']
	bundle['qmatrix%d-%s' % (k, train_power)] = qmatrix[k]
	maxi = len(nb_competences)
	ax.plot(range(1, len(qmatrix[k]) + 1), qmatrix[k], color='#ff%s00' % hex((i + 1) * 255 / maxi)[2:], linewidth=maxi - i)
# ax.plot(range(1, len(mepv_irt) + 1), mepv_irt, color='darkblue', linewidth=5)
ax.plot(range(1, len(irt) + 1), irt, color='blue', linewidth=5)
ax.set_title('IRT VS q-matrix K = 1-10, train_power %s' % train_power)
plt.show()

with open('bundle-%s.json' % folder, 'w') as f:
	f.write(json.dumps(bundle))

# nb_questions : 10, train_power : (80, 160)
# nb_questions : 40, train_power : (80, 160)

# train_power : (80, 160), courbes : 4, 6

"""
qmatrix = json.load(open('data/' + os.listdir('data')[-1]))['QMatrix']['mean']
irt = json.load(open('data/' + os.listdir('data')[-1]))['IRT']['mean']
#irt = json.load(open('data/stats-sat-19062014153953.moyenne-irt-30-80.json'))['IRT']['mean']
#qmatrix_bad = json.load(open('data/stats-sat-19062014150413.moyenne-qmatrix.json'))['QMatrix']['mean']
#qmatrix = json.load(open('data/stats-sat-19062014153507.moyenne-qmatrix-30-80.json'))['QMatrix']['mean']

# Fake data
# qmatrix = json.load(open('data/stats-fake_data-19062014163005.json'))['QMatrix']['mean']
# irt = json.load(open('data/stats-fake_data-19062014163005.json'))['IRT']['mean']

# Old data
# qmatrix_old = json.load(open('data/stats-sat-19062014164114.OMG.json'))['QMatrix']['mean']
# irt_old = json.load(open('data/stats-sat-19062014164114.OMG.json'))['IRT']['mean']

# Old data 2
# qmatrix = json.load(open('data/stats-sat-19062014164957.json'))['QMatrix']['mean']
# irt = json.load(open('data/stats-sat-19062014164957.json'))['IRT']['mean']

# Big data K = 5
# qmatrix = json.load(open('data/stats-sat-19062014190158.arf.5-comp.json'))['QMatrix']['mean']
# irt = json.load(open('data/stats-sat-19062014190158.arf.5-comp.json'))['IRT']['mean']

# Big data K = 4
# data = json.load(open('data/stats-sat-19062014191840.json'))

# Big data K = 4 α = 0.01
# data = json.load(open('data/stats-sat-19062014192051.json'))

# Big data K = 5 α = 0.01
# data = json.load(open('data/stats-sat-19062014192621.json'))

# Big data K = 5 α = 0.001
data = json.load(open('data/stats-sat-19062014195517.json'))
qmatrix = data['QMatrix']['mean']

# Big data K = 5 α = 0.000
data = json.load(open('data/stats-sat-19062014200009.json'))

qmatrix_zero = data['QMatrix']['mean']
irt = json.load(open('data/stats-sat-19062014192621.json'))['IRT']['mean']
qmatrix_old = json.load(open('data/stats-sat-19062014192621.json'))['QMatrix']['mean']

fig, ax = plt.subplots()
ax.plot(range(len(irt)), irt, color='blue')
ax.plot(range(len(qmatrix)), qmatrix, color='red')
ax.plot(range(len(qmatrix)), qmatrix_old, color='purple')
ax.plot(range(len(qmatrix)), qmatrix_zero, color='orange')
ax.set_title('Log loss, improved')
plt.show()
"""
