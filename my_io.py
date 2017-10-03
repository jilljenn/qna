import json
import os
from conf import PREFIX, DEBUG, STUDENT_FOLD, VERBOSE, QUESTION_FOLD
import random


def say(*something):
    if VERBOSE:
        print(' '.join(map(str, something)))


class IO(object):
    i = 0
    j = 0
    def __init__(self):
        if not os.path.exists(PREFIX):
            os.system('mkdir %s' % PREFIX)  # Maybe safer is better? :P
            os.system('mkdir %s/logs' % PREFIX)  # Maybe safer is better? :P
        for i in range(STUDENT_FOLD):
            for j in range(QUESTION_FOLD):
                self.update(i, j)
                if not os.path.exists(self.get_folder_name()):
                    os.system('mkdir %s' % self.get_folder_name())
        self.init()

    def get_folder_name(self):
        if self.i is not None:
            return '%s/%d-%d' % (PREFIX, self.i, self.j)
        else:
            return PREFIX

    def update(self, i, j=0, silent=False):
        self.i = i
        self.j = j
        if not silent:
            print('prefix is now', self.get_folder_name())

    def init(self):
        self.i = None
        self.j = None

    def backup(self, filename, data):
        with open('%s/%s.json' % (self.get_folder_name(), filename), 'w') as f:
            f.write(json.dumps(data))

    def load(self, filename, prefix=None):
        if not prefix:
            prefix = self.get_folder_name()
        return json.load(open('%s/%s.json' % (prefix, filename)))


class Dataset(object):
    name = None
    data = None
    nb_questions = None
    nb_students = None
    question_subset = None  # Deprecated
    train_subsets = None
    test_subsets = None
    STUDENT_FOLD = None
    QUESTION_FOLD = None
    validation_question_sets = None
    files = None
    def __init__(self, dataset_name, files=None):
        self.name = dataset_name
        self.files = files if files else IO()
        self.data = self.files.load(dataset_name, prefix='data')['student_data']
        self.nb_questions = len(self.data[0])
        self.nb_students = len(self.data)
        self.question_subset = list(range(self.nb_questions))  # All questions every time

    def get_triplets(self):
        return [(i, j, self.data[i][j]) for i in range(self.nb_students) for j in range(self.nb_questions)]

    def get_subset(self):
        from sklearn.model_selection import KFold, StratifiedKFold
        scores = [sum(student) for student in self.data]
        self.train_subsets = []
        self.test_subsets = []
        if DEBUG:
            all_students = list(range(len(self.data)))
            random.shuffle(all_students)
            train = all_students  # For debug
            test_student = train.pop()
            test = [test_student]
            self.train_subsets.append(sorted(train))
            self.test_subsets.append(test)
        else:
            kfold = StratifiedKFold(n_splits=STUDENT_FOLD, shuffle=True)
            for train, test in kfold.split(self.data, scores):
                self.train_subsets.append(train.tolist())
                self.test_subsets.append(test.tolist())
        self.validation_question_sets = []
        if QUESTION_FOLD >= 2:
            kfold = KFold(n_splits=QUESTION_FOLD, shuffle=True, random_state=None)
            for _, validation_question_array in kfold.split(self.data[0]):
                self.validation_question_sets.append(validation_question_array.tolist())
        else:
            self.validation_question_sets.append(list(range(self.nb_questions)))

    def to_dict(self):
        return {
            'question_subset': self.question_subset,
            'validation_question_sets': self.validation_question_sets,
            'train_subsets': self.train_subsets,
            'test_subsets': self.test_subsets,
        }

    def load_subset(self):
        subset = self.files.load('subset')
        self.question_subset = subset['question_subset']
        self.validation_question_sets = subset['validation_question_sets']
        self.train_subsets = subset['train_subsets']
        self.test_subsets = subset['test_subsets']

    def save_subset(self):
        self.files.backup('subset', self.to_dict())

    def __str__(self):
        return '[%s] (%d + %d) x %d, %dx%d-fold' % (self.name, len(self.train_subsets[0]), len(self.test_subsets[0]), self.nb_questions, len(self.train_subsets), len(self.validation_question_sets))
