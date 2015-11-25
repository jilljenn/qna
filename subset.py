from sklearn import cross_validation
import json
import random
from conf import dataset_name, nb_competences_values

STUDENT_TEST_SET_LENGTH = 10

if dataset_name == 'castor6e':
    question_subset = range(17)
    train_subset = sorted(random.sample(range(58939), 48939))
elif dataset_name == 'fraction':
    question_subset = range(20)
    nb_questions = len(question_subset)
    # train_subset = sorted(random.sample(range(536), 436))
    validation_question_sets = []
    for _, validation_question_array in cross_validation.KFold(n=nb_questions, n_folds=4, shuffle=True, random_state=None):
        validation_question_sets.append(validation_question_array.tolist())
    train_subset = sorted(random.sample(range(536), 536 - STUDENT_TEST_SET_LENGTH))
elif dataset_name == 'sat':
    question_subset = range(20)
    train_subset = sorted(random.sample(range(296), 216))
elif dataset_name == 'functional-analysis':
    question_subset = range(21)
    train_subset = sorted(random.sample(range(2287), 1800))
elif dataset_name == 'moodle':
    question_subset = range(15)
    train_subset = sorted(random.sample(range(2350), 1800))

with open('subset.json', 'w') as f:
    f.write(json.dumps({
        'question_subset': question_subset,
        'validation_question_sets': validation_question_sets,
        'train_subset': train_subset
    }))
