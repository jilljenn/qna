# coding=utf8
from __future__ import unicode_literals
import sys, os, re, json
import matplotlib
matplotlib.use('pgf')
pgf_with_rc_fonts = {
	'font.family': 'serif',
	'font.serif': [],
	'text.usetex': True,
	'text.latex.unicode': True,
}
matplotlib.rcParams.update(pgf_with_rc_fonts)
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob
from conf import PREFIX, nb_competences_values, model_names
from style import color, fmt, main_label, main_linewidth, get_label

displayed_y_axis = sys.argv[2]  # 'mean' or 'count'

from matplotlib.backends.backend_pdf import PdfPages
# pp = PdfPages('plot.pdf')

results = {}

folder = sys.argv[1]
BW = False

full_dataset = {
	'sat': 'SAT',
	'fraction': 'Fraction',
	'ecpe': 'ECPE',
	'timss2003': 'TIMSS',
	'castor6e': 'Castor',
}

ylabel = {
	# 'count': 'Nombre de prédictions incorrectes',
	'count': 'Number of incorrect predictions',
	# 'mean': 'Log loss',
	'mean': 'Log-loss',
	# 'delta': 'Distance au diagnostic final',
	'delta': 'Distance to the final diagnosis',
}

all_datasets = []
for filename in glob.glob('data/*.json'):
	all_datasets.append(filename[len('data/'):-len('.json')])

for filename in os.listdir(folder):
	if filename.startswith('stats'):
		print(filename)
		dataset_name, name, nb_questions, dim = re.match('stats-(%s)-([a-z0-9-]+)-([0-9]+)-([0-9]+)-' % '|'.join(all_datasets), filename).groups()
		nb_questions = int(nb_questions)
		data = json.load(open('%s/%s' % (folder, filename)))['QMatrix' if len(name) <= 2 else model_names[name]][displayed_y_axis]
		# print name, nb_questions, dim
		results[(name, dim)] = data
for line in results:
	print(line)

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
for (name, dim) in sorted(results):
	names.append(name)
	curves[name], errorbar[name] = zip(*results[(name, dim)])
	curve = ax.errorbar(range(1, len(curves[name]) + 1), curves[name], yerr=errorbar[name], color=color[name] if not BW else 'black', linewidth=get_linewidth(name, dim), label=get_label(name, dim), fmt=fmt[name])  # linewidth[name]
	handles.append(curve)
# title = 'Comparaison de %s de tests adaptatifs (%s)' % ('stratégies' if 'dpp' in names else 'modèles', full_dataset[dataset_name])
title = 'Comparison of %s of subset selection (%s)' % ('strategies' if 'dpp' in names else 'models', full_dataset[dataset_name])
print(title)
ax.set_title(title)
# ax.set_xlabel('Nombre initial de questions posées')
ax.set_xlabel('Initial number of questions asked')
ax.set_ylabel(ylabel[displayed_y_axis])
# print(results, handles)
plt.legend(handles=handles)
plt.savefig('%s/%s-%s.pdf' % (folder, dataset_name, displayed_y_axis), format='pdf')
# plt.show()
