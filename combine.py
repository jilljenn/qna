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
                    model_name, nb_questions, dim = m.groups()
                else:
                    print(filename)
                #dim = 3
                data[model_name, dim] = {'nb_questions': nb_questions, 'dim': dim, 'dataset_name': dataset_name}
                report = files.load(filename.replace('.json', ''))
                print(filename, len(report), 'reports found')
                if model_name not in reports:
                    reports[model_name, dim] = {'dim': report.get('dim', 13)}
                for category in ['mean_error', 'nb_mistakes']:
                    reports[model_name, dim].setdefault(category, []).extend(report[category])  # Combine
files.init()
for model_name, dim in reports:
    dataset_name, nb_questions, dim = data[model_name, dim]['dataset_name'], data[model_name, dim]['nb_questions'], data[model_name, dim]['dim']
    files.backup('log-%s-%s-%s-%s-%s' % (dataset_name, model_name, nb_questions, dim, datetime.now().strftime('%d%m%Y%H%M%S')), reports[model_name, dim])
    print(model_name, len(reports[model_name, dim]))
