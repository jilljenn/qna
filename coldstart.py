# coding=utf-8
from mirt import MIRT
from qmatrix import QMatrix
from calc import logloss, avgstd
from conf import dataset_name, BATCH_SIZE
from my_io import IO, Dataset, say
import random
import numpy as np


def full_logloss(performance, truth):
    return logloss(performance, truth, range(len(performance)))

def hinge(performance, truth):
    nb_questions = len(performance)
    return sum(np.round(performance)[i] == truth[i] for i in range(nb_questions))


def simulate(train_data, test_data):
    q = QMatrix()
    q.load('qmatrix-%s' % dataset_name)
    model = MIRT(q=q)
    # model = MIRT(dim=8)
    model.training_step(train_data)
    nb_students = len(test_data)
    nb_questions = len(test_data[0])
    error_log = {'random': [], 'dpp': [], 'cat': []}
    chosen_once = random.sample(range(nb_questions), BATCH_SIZE)
    # error_rate = [[] for _ in range(budget)]
    for student_id in range(nb_students):
        truth = np.array(test_data[student_id])
        if student_id % 10 == 0:
            print(student_id)
        say('Étudiant', student_id, test_data[student_id])

        # Random
        model.init_test()
        chosen = chosen_once  # random.sample(range(nb_questions), BATCH_SIZE)
        # print('Random', chosen)
        answers = truth[chosen]
        model.bootstrap(chosen, answers)
        performance = model.predict_performance()
        error_log['random'].append(full_logloss(performance, truth))

        say(full_logloss(performance, truth))
        say(hinge(performance, truth), 'correct out of', nb_questions)

        # DPP
        model.init_test()
        chosen = model.select_batch(BATCH_SIZE)
        # print('DPP', chosen)
        answers = np.array(test_data[student_id])[chosen]
        model.bootstrap(chosen, answers)
        performance = model.predict_performance()
        error_log['dpp'].append(full_logloss(performance, truth))

        say(full_logloss(performance, truth))
        say(hinge(performance, truth), 'correct out of', nb_questions)

        # CAT
        model.init_test()
        budget = BATCH_SIZE
        replied_so_far = []
        results_so_far = []
        for t in range(1, budget + 1):
            question_id = model.next_item(replied_so_far, results_so_far)
            # say('\nRound', t, '-> We ask question', question_id + 1, 'to the examinee.')
            # say('Correct!' if test_data[student_id][question_id] else 'Incorrect.') #, "I expected: %f." % round(
            replied_so_far.append(question_id)
            results_so_far.append(test_data[student_id][question_id])
            model.estimate_parameters(replied_so_far, results_so_far)
            performance = model.predict_performance()

            # say(' '.join(map(lambda x: str(int(10 * round(x, 1))), performance)))
            # say('Estimate:', ''.join(map(lambda x: '%d' % int(round(x)), performance)))
            # say('   Truth:', ''.join(map(lambda x: '%d' % int(x), test_data[student_id])))
            # say(full_logloss(performance, truth))
        error_log['cat'].append(full_logloss(performance, truth))

        say(full_logloss(performance, truth))
        say(hinge(performance, truth), 'correct out of', nb_questions)


    """for strategy in error_log:
        print(error_log[strategy])"""
    for strategy in ['random', 'dpp', 'cat']:
        if len(error_log[strategy]) > 0:
            print(avgstd(error_log[strategy]))


def main():
    files = IO()
    dataset = Dataset(dataset_name, files)
    dataset.load_subset()
    print(dataset)
    train_dataset = [dataset.data[i] for i in dataset.train_subset]
    test_dataset = [dataset.data[i] for i in dataset.test_subset]
    simulate(train_dataset, test_dataset)


if __name__ == '__main__':
    main()
