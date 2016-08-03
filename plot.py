# coding=utf8
import sys, os, re, json
import matplotlib.pyplot as plt
import glob
from conf import nb_competences_values, model_names

from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('plot.pdf')

results = {}

folder = sys.argv[1]
BW = False

all_datasets = []
for filename in glob.glob('data/*.json'):
	all_datasets.append(filename[len('data/'):-len('.json')])

for filename in os.listdir(folder):
	if filename.startswith('stats'):
		print filename
		dataset_name, name, nb_questions, train_power = re.match('stats-(%s)-([a-z0-9-]+)-([0-9]+)-([0-9]+)-' % '|'.join(all_datasets), filename).groups()
		nb_questions = int(nb_questions)
		data = json.load(open('%s/%s' % (folder, filename)))['QMatrix' if len(name) <= 2 else model_names[name]]['mean']
		# print name, nb_questions, train_power
		results[(name, train_power)] = data
for line in results:
	print(line)

color = {'3': 'red', '4': 'orangered', '5': 'orange', '6': 'yellow', '8': 'blue', 'irt': 'red', 'mepv-irt': 'darkblue', 'baseline': 'darkgreen', '888': 'green', 'mirt': 'red', 'qm': 'blue', 'qm-qmatrix-cdm': 'green', 'mirt-qm-matrix-cdm-new': 'gold'}
fmt = {'irt': '.', 'mirt-qm-qmatrix-cdm': '+', 'mirt-qm-qmatrix-cdm-new': 's', 'mirt': '+', 'qm': 'o'}
# linewidth = {'mirt': 5, '888': 3, '8': 3, 'irt': 1, 'qm': 3, 'qm-qmatrix-cdm': 3, 'mirt-qm-qmatrix-cdm': 5, 'mirt-qm-qmatrix-cdm-new': 7, 'mirt-qm-qmatrix-cdm-new': 7}
linewidth = {'irt': 2, 'mirt-qm-qmatrix-cdm-new': 3}
label = {'irt': 'Rasch', 'qm-qmatrix-cdm': 'DINA', 'mirt-qm-qmatrix-cdm-new': 'GenMA + auto', 'mirt': 'MIRT', 'qm': 'DINA auto'}
for qmatrix_name in ['cdm', 'ecpe', 'banach', 'fraction', 'custom', 'cdm-new']:
	for prefix in ['qm', 'mirt-qm']:
		tag = '%s-qmatrix-%s' % (prefix, qmatrix_name)
		color[tag] = 'red' if prefix == 'mirt-qm' else 'green'
		# linewidth[tag] = 5 if prefix == 'mirt-qm' else 3
		label[tag] = 'GenMA + expert' if prefix == 'mirt-qm' else 'DINA'
		fmt[tag] = 'o' if prefix == 'mirt-qm' else '+'

# plt.style.use('ggplot')
fig, ax = plt.subplots()

curves = {}
errorbar = {}

handles = []
for (name, train_power) in results:
	curves[name], errorbar[name] = zip(*results[(name, train_power)])
	curve = ax.errorbar(range(1, len(curves[name]) + 1), curves[name], yerr=errorbar[name], color=color[name] if not BW else 'black', linewidth=linewidth.get(name, 2), label=label[name], fmt='-' + fmt[name])  # linewidth[name]
	handles.append(curve)
ax.set_title('Comparing models for adaptive testing (dataset: %s)' % dataset_name)
ax.set_xlabel('Number of questions asked')
ax.set_ylabel('Incorrect predictions count' if folder == 'ectel0' else 'Mean error')
print(results, handles)
plt.legend(handles=handles)
plt.savefig('plot.png', format='png')
plt.show()
