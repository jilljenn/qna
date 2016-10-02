# coding=utf8
import sys, os, re, json
import matplotlib
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob
from conf import PREFIX, nb_competences_values, model_names

displayed_y_axis = sys.argv[2]  # 'mean' or 'count'

from matplotlib.backends.backend_pdf import PdfPages
# pp = PdfPages('plot.pdf')

results = {}

folder = sys.argv[1]
BW = False

color = {
	'3': 'red',
	'4': 'orangered',
	'5': 'orange',
	'6': 'yellow',
	'8': 'blue',
	'irt': 'red',
	'mepv-irt': 'darkblue',
	'baseline': 'darkgreen',
	'888': 'green',
	'mirt': 'red',
	'qm': 'blue',
	'qm-qmatrix-cdm': 'green',
	'mirt-qm-matrix-cdm-new': 'gold',
	'random': 'blue',
	'dpp': 'red',
	'cat': 'green',
	'uncertainty': 'black'
}

fmt = {
	'irt': '.',
	'mirt-qm-qmatrix-cdm': '+',
	'mirt-qm-qmatrix-cdm-new': 's',
	'mirt': '+',
	'qm': '^',
	'dpp': '+',
	'random': '^',
	'cat': 'o',
	'uncertainty': '.'
}

main_label = {
	'irt': 'Rasch',
	'qm-qmatrix-cdm': 'DINA',
	'mirt': 'MIRT',
	'qm': 'DINA auto',
	'cat': 'CAT',
	'dpp': 'InitialD',
	'uncertainty': 'Uncertainty',
	'random': 'Random'
}

def get_label(name, dim):
	label = main_label[name]
	if name == 'qm':
		label += ' K = %s' % dim
	return label

ylabel = {
	'count': 'Incorrect predictions count',
	'mean': 'Mean error',
	'delta': 'Distance to true parameter',
}

all_datasets = []
for filename in glob.glob('data/*.json'):
	all_datasets.append(filename[len('data/'):-len('.json')])

for filename in os.listdir(folder):
	if filename.startswith('stats'):
		print filename
		dataset_name, name, nb_questions, dim = re.match('stats-(%s)-([a-z0-9-]+)-([0-9]+)-([0-9]+)-' % '|'.join(all_datasets), filename).groups()
		nb_questions = int(nb_questions)
		data = json.load(open('%s/%s' % (folder, filename)))['QMatrix' if len(name) <= 2 else model_names[name]][displayed_y_axis]
		# print name, nb_questions, dim
		results[(name, dim)] = data
for line in results:
	print(line)

# linewidth = {'mirt': 5, '888': 3, '8': 3, 'irt': 1, 'qm': 3, 'qm-qmatrix-cdm': 3, 'mirt-qm-qmatrix-cdm': 5, 'mirt-qm-qmatrix-cdm-new': 7, 'mirt-qm-qmatrix-cdm-new': 7}
main_linewidth = {'irt': 2, 'mirt-qm-qmatrix-cdm-new': 3}
for qmatrix_name in ['cdm', 'ecpe', 'banach', 'fraction', 'custom', 'cdm-new', 'fake', 'timss2003', 'castor6e', 'sat', 'sat2', 'sat3', 'sat4']:
	for prefix in ['qm', 'mirt-qm']:
		tag = '%s-qmatrix-%s' % (prefix, qmatrix_name)
		color[tag] = 'red' if prefix == 'mirt-qm' else 'green'
		# linewidth[tag] = 5 if prefix == 'mirt-qm' else 3
		main_label[tag] = 'GenMA + expert' if prefix == 'mirt-qm' else 'DINA'
		fmt[tag] = 'o' if prefix == 'mirt-qm' else '+'
main_label['mirt-qm-qmatrix-cdm-new'] = 'GenMA + auto'

all_dim = set()
for (name, dim) in results:
	if name == 'qm':
		all_dim.add(dim)
all_dim = sorted(all_dim)

def get_linewidth(name, dim):
	if name in main_linewidth:
		return main_linewidth[name]
	elif name == 'qm':
		return 2 + all_dim.index(dim)
	else: 
		return 2

# plt.style.use('ggplot')
fig, ax = plt.subplots()

curves = {}
errorbar = {}

handles = []
names = []
for (name, dim) in results:
	names.append(name)
	curves[name], errorbar[name] = zip(*results[(name, dim)])
	curve = ax.errorbar(range(1, len(curves[name]) + 1), curves[name], yerr=errorbar[name], color=color[name] if not BW else 'black', linewidth=get_linewidth(name, dim), label=get_label(name, dim), fmt='-' + fmt[name])  # linewidth[name]
	handles.append(curve)
ax.set_title('Comparing %s for adaptive testing (dataset: %s)' % ('strategies' if 'dpp' in names else 'models', dataset_name))
ax.set_xlabel('Number of questions asked')
ax.set_ylabel(ylabel[displayed_y_axis])
# print(results, handles)
plt.legend(handles=handles)
plt.savefig('%s/plot-%s.pdf' % (folder, displayed_y_axis), format='pdf')
# plt.show()
