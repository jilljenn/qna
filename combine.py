# coding=utf-8
from conf import dataset_name, STUDENT_FOLD, QUESTION_FOLD
from my_io import IO
from datetime import datetime
import os
import re

def make_stats(log):
    nb_students = len(log)
    budget = len(log[0])
    results

files = IO()
reports = {}
data = {}
for i in range(STUDENT_FOLD):
    for j in range(QUESTION_FOLD):
        files.update(i, j)
        for filename in os.listdir(files.get_folder_name()):
            if filename.startswith('log'):
                m = re.match('log-%s-([a-z0-9-]+)-([0-9]+)-([0-9]+)-' % dataset_name, filename)
                if m:
                    model_name, nb_questions, train_power = m.groups()
                else:
                    print(filename)
                data[model_name] = {'nb_questions': nb_questions, 'train_power': train_power, 'dataset_name': dataset_name}
                report = files.load(filename.replace('.json', ''))
                print filename, len(report), 'reports found'
                if model_name not in reports:
                    reports[model_name] = {}
                for category in ['mean_error', 'nb_mistakes']:
                    reports[model_name].setdefault(category, []).extend(report[category])  # Combine
files.init()
for model_name in reports:
    dataset_name, nb_questions, train_power = data[model_name]['dataset_name'], data[model_name]['nb_questions'], data[model_name]['train_power']
    files.backup('log-%s-%s-%s-%s-%s' % (dataset_name, model_name, nb_questions, train_power, datetime.now().strftime('%d%m%Y%H%M%S')), reports[model_name])
    print model_name, len(reports[model_name])
