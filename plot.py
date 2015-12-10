# coding=utf8
import sys, os, re, json
import matplotlib.pyplot as plt
from conf import dataset_name, nb_competences_values

"""
loglosses_ltm = json.load(open('data/logloss-ltm.json'))
loglosses_qmatrix = json.load(open('data/logloss-qmatrix.json'))

fig, ax = plt.subplots()
ax.plot(range(len(loglosses_ltm)), loglosses_ltm, color='blue')
ax.plot(range(len(loglosses_qmatrix)), loglosses_qmatrix, color='red')
ax.set_title('Log loss')
plt.show()
"""

if dataset_name == 'sat':
	train_power = '216'
elif dataset_name == 'castor6e':
	train_power = '48939'
elif dataset_name == 'fraction':
	train_power = '436'
elif dataset_name == 'functional-analysis':
	train_power = '1800'
elif dataset_name == 'moodle':
	train_power = '1800'	
else:
	train_power = '90'

graphs = {'20': {}, '40': {}, '80': {}, '90': {}, '160': {}, '216': {}, '276': {}, '286': {}, '295': {}, '48939': {}, '99': {}, '436': {}, '526': {}, '535': {}, '1800': {}}
graphs2 = {10: {}, 15: {}, 20: {}, 30: {}, 40: {}, 17: {}, 3: {}, 21: {}}
modelnames = {'irt': 'IRT', 'mepv-irt': 'IRT', 'baseline': 'Baseline', '888': 'QMatrix', 'mirt': 'MIRT'}
filenames = {}

folder = sys.argv[1]

for filename in os.listdir(folder):
	if filename.startswith('stats'):
		print filename
		name, nb_questions, train_power = re.match('stats-%s-([a-z0-9-]+)-([0-9]+)-([0-9]+)-' % dataset_name, filename).groups()
		nb_questions = int(nb_questions)
		data = json.load(open('%s/%s' % (folder, filename)))['QMatrix' if len(name) <= 2 else modelnames[name]]['mean']
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

colors = {'3': 'red', '4': 'orangered', '5': 'orange', '6': 'yellow', 'irt': 'blue', 'mepv-irt': 'darkblue', 'baseline': 'darkgreen'}

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
irt, irt_err = zip(*json.load(open(filenames[('irt', train_power)]))['IRT']['mean'])
qmspe, qmspe_err = zip(*json.load(open(filenames[('888', train_power)]))['QMatrix']['mean'])
mirt, mirt_err = zip(*json.load(open(filenames[('mirt', train_power)]))['MIRT']['mean'])
# mepv_irt = json.load(open(filenames[('mepv-irt', train_power)]))['IRT']['mean']
# baseline = json.load(open(filenames[('baseline', train_power)]))['Baseline']['mean']
bundle['irt-%s' % train_power] = irt
# bundle['qmatrix888-%s' % train_power] = qmspe
qmatrix = {}
qmatrix_spe = {}
ax.errorbar(range(1, len(irt) + 1), irt, yerr=irt_err, color='blue', linewidth=5)
ax.errorbar(range(1, len(mirt) + 1), mirt, yerr=mirt_err, color='red', linewidth=5)
ax.errorbar(range(1, len(qmspe) + 1), qmspe, yerr=qmspe_err, color='darkgreen', linewidth=5)
for i, k in enumerate(nb_competences_values):
	print('plot', i, k)
	qmatrix[k], qmatrix_spe[k] = zip(*json.load(open(filenames[(str(k), train_power)]))['QMatrix']['mean'])
	bundle['qmatrix%d-%s' % (k, train_power)] = qmatrix[k]
	maxi = len(nb_competences_values)
	ax.errorbar(range(1, len(qmatrix[k]) + 1), qmatrix[k], yerr=qmatrix_spe[k], color='#ff%s00' % '00', linewidth=maxi - i)  # hex((i + 1) * 255 / maxi)[2:]
# ax.plot(range(1, len(mepv_irt) + 1), mepv_irt, color='darkblue', linewidth=5)
# ax.plot(range(1, len(baseline) + 1), baseline, color='darkgreen', linewidth=3)
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
