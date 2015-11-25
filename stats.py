from my_io import IO
from conf import dataset_name
from cat import get_results
import os
import re

model_names = {
    'irt': 'IRT',
    '8': 'QMatrix',
    '888': 'QMatrix'
}

io_handler = IO()
io_handler.update(0)
for filename in os.listdir(io_handler.prefix):
    if filename.startswith('log') and not os.path.exists('%s/%s' % (io_handler.prefix, filename.replace('log', 'stats'))):
        name, nb_questions, train_power = re.match('log-%s-([a-z0-9-]+)-([0-9]+)-([0-9]+)-' % dataset_name, filename).groups()
        model_name = model_names[name]
        god_prefix = '%s-%s-%s' % (name, nb_questions, train_power)
        log = {}
        if raw_input('Do you want to rebuild stats for %s? ' % filename) == 'y':
            log[model_name] = io_handler.load(filename.replace('.json', ''))
            get_results(log, god_prefix, io_handler)
