import json
import os
from conf import PREFIX, DEBUG, STUDENT_TEST_RATE, VERBOSE, VALIDATION_FOLD
import random

def say(*something):
    if VERBOSE:
        print(' '.join(map(str, something)))


class IO(object):
    def __init__(self):
        self.prefix = PREFIX + '0'
        for i in range(0, VALIDATION_FOLD + 1):
            self.update(i)
            if not os.path.exists(self.prefix):
                os.system('mkdir %s' % self.prefix)
        self.update(0)
        # filename = '%s/%s' % (self.prefix, 'qmatrix-cdm.json')
        # if not os.path.exists(filename):
        #    os.system('cp qmatrix-cdm.json %s' % filename)

    def update(self, step):
        prefix = list(self.prefix)
        prefix[-1] = str(step)
        self.prefix = ''.join(prefix)
        print 'prefix is now', self.prefix

    def split(self, filename, n):
        """Creates files and returns filenames."""
        dataset = load(filename)['student_data']
        chunk_length = (len(dataset) - len(dataset) % n) / n
        bundle = []
        for k in range(n):
            train, test = [], []
            for i, line in enumerate(dataset):
                if k * chunk_length <= i < (k + 1) * chunk_length:
                    test.append(line)
                else:
                    train.append(line)
            bundle.append((train, test))
        return bundle

    def backup(self, filename, data):
        with open('%s/%s.json' % (self.prefix, filename), 'w') as f:
            f.write(json.dumps(data))

    def load(self, filename, prefix=None):
        if not prefix:
            prefix = self.prefix
        return json.load(open('%s/%s.json' % (prefix, filename)))


class Dataset(object):
    name = None
    data = None
    nb_questions = None
    nb_students = None
    question_subset = None
    train_subset = None
    test_subset = None
    validation_question_sets = None
    files = None
    def __init__(self, dataset_name, files=None):
        self.name = dataset_name
        self.files = files if files else IO()
        self.data = self.files.load(dataset_name, prefix='data')['student_data']
        self.nb_questions = len(self.data[0])
        self.nb_students = len(self.data)
        self.question_subset = range(self.nb_questions)

    def get_subset(self):
        from sklearn import cross_validation
        student_test_length = 1 if DEBUG else int(round(STUDENT_TEST_RATE * self.nb_students))
        student_train_length = self.nb_students - student_test_length
        self.train_subset = sorted(random.sample(range(self.nb_students), student_train_length))
        self.test_subset = list(set(range(self.nb_students)) - set(self.train_subset))
        self.validation_question_sets = []
        for _, validation_question_array in cross_validation.KFold(n=self.nb_questions, n_folds=VALIDATION_FOLD, shuffle=True, random_state=None):
            self.validation_question_sets.append(validation_question_array.tolist())
            # break  # TODO REMOVE THIS break OR WE ARE ALL DEAD

    def to_dict(self):
        return {
            'question_subset': self.question_subset,
            'validation_question_sets': self.validation_question_sets,
            'train_subset': self.train_subset,
            'test_subset': self.test_subset
        }

    def load_subset(self):
        subset = self.files.load('subset')
        self.question_subset = subset['question_subset']
        self.validation_question_sets = subset['validation_question_sets']
        self.train_subset = subset['train_subset']
        self.test_subset = subset['test_subset']

    def save_subset(self):
        self.files.backup('subset', self.to_dict())

    def __str__(self):
        return '[%s] (%d + %d) x %d, %d VQ' % (self.name, len(self.train_subset), len(self.test_subset), self.nb_questions, len(self.validation_question_sets))
