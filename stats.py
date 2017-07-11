from my_io import IO
from conf import dataset_name, model_names
from cat import get_results
import os
import re

files = IO()
files.init()
for filename in os.listdir(files.get_folder_name()):
    if filename.startswith('log') and not filename.startswith('logs') and not os.path.exists('%s/%s' % (files.get_folder_name(), filename.replace('log', 'stats'))):  # No stats for these reports
        regexp = 'log-%s-([a-z0-9-]+)-([0-9]+)-([0-9]+)-' % dataset_name
        name, nb_questions, train_power = re.match(regexp, filename).groups()
        model_name = model_names[name]
        god_prefix = '%s-%s-%s' % (name, nb_questions, train_power)

        if input('Do you want to rebuild stats for %s? ' % filename) == 'y':
            report = files.load(filename.replace('.json', ''))
            report['model_name'] = model_name
            get_results(report, god_prefix, files)
