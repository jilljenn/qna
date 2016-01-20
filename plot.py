# coding=utf8
import sys, os, re, json
import matplotlib.pyplot as plt
from conf import dataset_name, nb_competences_values, model_names

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

results = {}

folder = sys.argv[1]

for filename in os.listdir(folder):
	if filename.startswith('stats'):
		print filename
		name, nb_questions, train_power = re.match('stats-%s-([a-z0-9-]+)-([0-9]+)-([0-9]+)-' % dataset_name, filename).groups()
		nb_questions = int(nb_questions)
		data = json.load(open('%s/%s' % (folder, filename)))['QMatrix' if len(name) <= 2 else model_names[name]]['mean']
		# print name, nb_questions, train_power
		results[(name, train_power)] = data

color = {'3': 'red', '4': 'orangered', '5': 'orange', '6': 'yellow', '8': 'blue', 'irt': 'red', 'mepv-irt': 'darkblue', 'baseline': 'darkgreen', '888': 'green', 'mirt': 'red', 'qm': 'blue', 'qm-qmatrix-cdm': 'green', 'mirt-qm-qmatrix-cdm': 'red', 'mirt-qm-qmatrix-custom': 'gold'}
linewidth = {'mirt': 5, '888': 3, '8': 3, 'irt': 1, 'qm': 3, 'qm-qmatrix-cdm': 3, 'mirt-qm-qmatrix-cdm': 5, 'mirt-qm-qmatrix-custom': 5}

fig, ax = plt.subplots()

curves = {}
errorbar = {}

for (name, train_power) in results:
	curves[name], errorbar[name] = zip(*results[(name, train_power)])
	ax.errorbar(range(1, len(curves[name]) + 1), curves[name], yerr=errorbar[name], color=color[name], linewidth=linewidth[name])
ax.set_title('Comparing models for adaptive testing')
plt.show()
