# coding=utf8
import sys, os, re, json
import matplotlib.pyplot as plt
from conf import dataset_name, nb_competences_values, model_names

from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('plot.pdf')

results = {}

folder = sys.argv[1]
BW = True

for filename in os.listdir(folder):
	if filename.startswith('stats'):
		print filename
		dataset_name, name, nb_questions, train_power = re.match('stats-(%s)-([a-z0-9-]+)-([0-9]+)-([0-9]+)-' % dataset_name, filename).groups()
		nb_questions = int(nb_questions)
		data = json.load(open('%s/%s' % (folder, filename)))['QMatrix' if len(name) <= 2 else model_names[name]]['mean']
		# print name, nb_questions, train_power
		results[(name, train_power)] = data

color = {'3': 'red', '4': 'orangered', '5': 'orange', '6': 'yellow', '8': 'blue', 'irt': 'red', 'mepv-irt': 'darkblue', 'baseline': 'darkgreen', '888': 'green', 'mirt': 'red', 'qm': 'blue', 'qm-qmatrix-cdm': 'green', 'mirt-qm-qmatrix-cdm': 'red', 'mirt-qm-qmatrix-custom': 'gold'}
linewidth = {'mirt': 5, '888': 3, '8': 3, 'irt': 1, 'qm': 3, 'qm-qmatrix-cdm': 3, 'mirt-qm-qmatrix-cdm': 5, 'mirt-qm-qmatrix-custom': 5}
label = {'mirt-qm-qmatrix-cdm': 'GenMA', 'irt': 'Rasch', 'qm-qmatrix-cdm': 'DINA'}

fig, ax = plt.subplots()

curves = {}
errorbar = {}

handles = []
for (name, train_power) in results:
	curves[name], errorbar[name] = zip(*results[(name, train_power)])
	curve = ax.errorbar(range(1, len(curves[name]) + 1), curves[name], yerr=errorbar[name], color=color[name] if not BW else 'black', linewidth=linewidth[name], label=label[name])
	handles.append(curve)
ax.set_title('Comparing models for adaptive testing (dataset: %s)' % dataset_name)
plt.legend(handles=handles)
plt.savefig('plot.png', format='png')
# plt.show()
