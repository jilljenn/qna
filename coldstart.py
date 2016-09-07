# coding=utf-8
from datetime import datetime
from mirt import MIRT
from qmatrix import QMatrix
from calc import logloss, avgstd
from conf import dataset_name, STUDENT_FOLD, strategies
from cat import get_results
from my_io import IO, Dataset, say
import random
import numpy as np


def full_logloss(performance, truth):
    return logloss(performance, truth, range(len(performance)))

def hinge(performance, truth):
    nb_questions = len(performance)
    return sum(np.round(performance)[i] == truth[i] for i in range(nb_questions))

def get_delta(theta1, theta2):
    return np.linalg.norm(np.array(theta1) - np.array(theta2))


def simulate(train_data, test_data):
    q = QMatrix()
    q.load('qmatrix-%s' % dataset_name)
    model = MIRT(q=q)
    # model = MIRT(dim=8)
    model.training_step(train_data)
    nb_students = len(test_data)
    nb_questions = len(test_data[0])
    report = {strategy: {'delta': [], 'mean_error': [], 'model_name': strategy} for strategy in strategies + ['cat']}

    for student_id in range(nb_students):
        for strategy in strategies + ['cat']:
            for key in ['delta', 'mean_error']:
                report[strategy][key].append([])  # Data for new student

        truth = np.array(test_data[student_id])
        if student_id % 10 == 0:
            print(student_id)
        say('Étudiant', student_id, test_data[student_id])

        # True theta
        model.init_test()
        model.bootstrap(range(nb_questions), truth)  # Ask all questions get all answers
        true_theta = model.theta  # Record maximum likelihood estimate

        for nb_questions_asked in range(1, nb_questions + 1):
            for strategy in strategies:
                model.init_test()
                if strategy == 'random':  # Random
                    chosen = random.sample(range(nb_questions), nb_questions_asked)
                else:  # DPP
                    chosen = model.select_batch(nb_questions_asked)
                answers = truth[chosen]
                model.bootstrap(chosen, answers)
                performance = model.predict_performance()
                report[strategy]['mean_error'][student_id].append(full_logloss(performance, truth))
                report[strategy]['delta'][student_id].append(get_delta(model.theta, true_theta))

                say('mean_error', full_logloss(performance, truth))
                say(hinge(performance, truth), 'correct out of', nb_questions)
        # report[strategy]['mean_error'].reverse()
        # report[strategy]['delta'].reverse()

        # CAT
        model.init_test()
        replied_so_far = []
        results_so_far = []
        for t in range(1, nb_questions + 1):
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
            report['cat']['mean_error'][student_id].append(full_logloss(performance, truth))
            report['cat']['delta'][student_id].append(get_delta(model.theta, true_theta))

            say('mean_error', full_logloss(performance, truth))
            say(hinge(performance, truth), 'correct out of', nb_questions)
    return report


def main():
    files = IO()
    dataset = Dataset(dataset_name, files)
    dataset.load_subset()
    print(dataset)
    for i_exp in range(STUDENT_FOLD):
        files.update(i_exp)
        train_subset = dataset.train_subsets[i_exp]
        test_subset = dataset.test_subsets[i_exp]
        train_dataset = [[dataset.data[i][j] for j in dataset.question_subset] for i in train_subset]
        test_dataset = [[dataset.data[i][j] for j in dataset.question_subset] for i in test_subset]        
        report = simulate(train_dataset, test_dataset)
        for strategy in report:
            train_power = len(train_subset)
            filename = strategy + '-%s-%s' % (dataset.nb_questions, train_power)
            get_results(report[strategy], filename, files)
            files.backup('log-%s-%s-%s' % (dataset_name, filename, datetime.now().strftime('%d%m%Y%H%M%S')), report[strategy])


if __name__ == '__main__':
    main()
