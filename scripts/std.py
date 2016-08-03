# coding=utf8
import os, re, json, math
from conf import dataset_name

def avgstd(l): # Displays mean and variance
    n = len(l)
    # print 'computed over %d values' % n
    mean = float(sum(l)) / n
    var = float(sum(i * i for i in l)) / n - mean * mean
    return '%.3f $\pm$ %.3f' % (round(mean, 3), round(1.96 * math.sqrt(var / (10 * n)), 3))
    # return mean, round(1.96 * math.sqrt(var / n), 5)

if dataset_name == 'castor6e':
    NB_QUESTIONS = 17
    TRAIN_POWER = 48939
    FOLDERS = ['edm-castor']
    FILES = ['2', '5', '8', '11', '14', 'irt']
elif dataset_name == 'fraction':
    NB_QUESTIONS = 20
    TRAIN_POWER = 535
    FOLDERS = ['edm-fraction', 'edm-fraction2']
    FILES = ['2', '5', '8', '11', '14', 'irt', '888']
elif dataset_name == 'sat':
    NB_QUESTIONS = 20
    TRAIN_POWER = 216
    FOLDERS = ['edm-sat', 'edm-sat2']
    FILES = ['2', '5', '8', '11', '14', 'irt']

values = {}
for folder in FOLDERS:
    for filename in os.listdir(folder):
        if filename.startswith('log'):
            name, nb_questions, train_power = re.match('log-%s-([a-z0-9-]+)-([0-9]+)-([0-9]+)-' % dataset_name, filename).groups()
            nb_questions = int(nb_questions)
            train_power = int(train_power)
            data = json.load(open('%s/%s' % (folder, filename)))
            if nb_questions == NB_QUESTIONS:
                for line in data:
                    for nb_q in [4, 10, 16]:
                       values.setdefault((name, nb_q), []).append(line[nb_q - 1])
for name in FILES:
    print name, '&',
    for nb_q in [4, 10, 16]:
        print avgstd(values[(name, nb_q)]),
        if nb_q < 16:
            print '&',
        else:
            print '\\\\'
