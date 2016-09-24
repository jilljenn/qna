import sys, os, glob
import re, json
from conf import model_names

LATEX = True

results = {}
folder = sys.argv[1]
questions = map(lambda x: int(x) - 1, sys.argv[2].split(','))
value = sys.argv[3]
nb_validation = float(sys.argv[4])

all_datasets = []
for filename in glob.glob('data/*.json'):
    all_datasets.append(filename[len('data/'):-len('.json')])

for filename in os.listdir(folder):
    if filename.startswith('stats'):
        print filename
        dataset_name, name, nb_questions, train_power = re.match('stats-(%s)-([a-z0-9-]+)-([0-9]+)-([0-9]+)-' % '|'.join(all_datasets), filename).groups()
        nb_questions = int(nb_questions)
        data = json.load(open('%s/%s' % (folder, filename)))['QMatrix' if len(name) <= 2 else model_names[name]]#[displayed_y_axis]
        # print name, nb_questions, train_power
        results[(name, train_power)] = data

if LATEX:
    print(r'\begin{tabular}{c%s}' % ('c' * len(questions)))
    print(r'& ' + ' & '.join('After %d questions' % (q_index + 1) for q_index in questions) + r'\\')
    for key in results:
        model_name, _ = key
        if value == 'mean':
            elements = [r'$%s \pm %s$ (%d \%%)' % tuple(results[key]['mean'][q_index] + [round(100 * (1 - results[key]['count'][q_index][0] / nb_validation), 1)]) for q_index in questions]
        else:
            elements = [r'$%s \pm %s$' % tuple(results[key]['delta'][q_index]) for q_index in questions]
        print model_names[model_name], 'K = %s' % key[1], '&', ' & '.join(elements) + r'\\'
    print(r'\end{tabular}')
else:
    for key in results:
        model_name, _ = key
        print(model_name, [results[key]['mean'][q_index] if value == 'mean' else round(1 - results[key]['count'][q_index][0] / nb_validation, 3) for q_index in questions])
