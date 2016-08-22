from conf import dataset_name, VALIDATION_FOLD
from my_io import IO
from datetime import datetime
import os
import re

def make_stats(log):
    nb_students = len(log)
    budget = len(log[0])
    results

io_handler = IO()
logs = {}
data = {}
for i in range(1, VALIDATION_FOLD + 1):
    io_handler.update(i)
    for filename in os.listdir(io_handler.prefix):
        if filename.startswith('log'):
            m = re.match('log-%s-([a-z0-9-]+)-([0-9]+)-([0-9]+)-' % dataset_name, filename)
            if m:
                name, nb_questions, train_power = m.groups()
            else:
                print(filename)
            data[name] = {'nb_questions': nb_questions, 'train_power': train_power, 'dataset_name': dataset_name}
            log = io_handler.load(filename.replace('.json', ''))
            print filename, len(log), 'logs found'
            logs.setdefault(name, []).extend(log)
io_handler.update(0)
for name in logs:
    dataset_name, nb_questions, train_power = data[name]['dataset_name'], data[name]['nb_questions'], data[name]['train_power']
    io_handler.backup('log-%s-%s-%s-%s-%s' % (dataset_name, name, nb_questions, train_power, datetime.now().strftime('%d%m%Y%H%M%S')), logs[name])
    print(name, len(logs[name]))
