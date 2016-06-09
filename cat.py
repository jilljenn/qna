# coding=utf8
from datetime import datetime
from calc import logloss, surround, avgstd
from conf import dataset_name, nb_competences_values
from my_io import IO, Dataset, say
import random
import json
import sys

def display(results):
	for name in results:
		print name, results[name]['mean']

def evaluate(performance, truth, validation_question_set):
	nb_questions = len(performance)
	# print [performance[i] for i in range(nb_questions) if i not in replied_so_far], [truth[i] for i in range(nb_questions) if i not in replied_so_far]
	# return logloss([performance[i] for i in range(nb_questions) if i not in replied_so_far], [truth[i] for i in range(nb_questions) if i not in replied_so_far])
	# return 0 if not validation_question_set else sum(round(performance[i]) != truth[i] for i in validation_question_set)
	return logloss(performance, truth, validation_question_set)

def dummy_count(performance, truth, replied_so_far):
	nb_questions = len(performance)
	# print 'indecision', sum([0.4 <= performance[i] <= 0.6 for i in range(nb_questions) if i not in replied_so_far])
	return sum([(performance[i] < 0.5 and truth[i]) or (performance[i] > 0.5 and not truth[i]) for i in range(nb_questions) if i not in replied_so_far]) # Count errors

def get_results(log, god_prefix, files):
	results = {}
	nb_students = len(log.values()[0])
	budget = len(log.values()[0][0])
	for model_name in log:
		# print model.name
		results[model_name] = {'mean': [avgstd([log[model_name][i][t] for i in range(nb_students)]) for t in range(budget)]}
		"""for t in range(budget):
			print(avgstd(list(log[model.name][i][t] for i in range(nb_students))))"""
	files.backup('stats-%s-%s-%s' % (dataset_name, god_prefix, datetime.now().strftime('%d%m%Y%H%M%S')), results)

def simulate(model, train_data, test_data, validation_question_set, error_log):
	model.training_step(train_data, opt_Q=True, opt_sg=True)

	say(datetime.now())
	say('=' * 10, model.name)

	nb_students = len(test_data)
	nb_questions = len(test_data[0])
	budget = nb_questions - len(validation_question_set)
	if all_student_sampled:
		student_sample = range(nb_students) # All students
	error_rate = [[] for _ in range(budget)]
	for student_id in student_sample:
		if student_id % 10 == 0:
			print(student_id)

		say('Étudiant', student_id, test_data[student_id])

		error_log.append([0] * budget)
		model.init_test(validation_question_set=validation_question_set)
		replied_so_far = []
		results_so_far = []

		say('Estimation initiale :', map(lambda x: round(x, 1), model.predict_performance()))
		say('Erreur initiale :', logloss(model.predict_performance(), test_data[student_id]))

		for t in range(1, budget + 1):
			question_id = model.next_item(replied_so_far, results_so_far)

			say('\nRound', t, '-> We ask question', question_id + 1, 'to the examinee.')
			if model.name == 'IRT':
				say('Difficulty:', model.coeff.rx(question_id + 1)[0])
			elif model.name == 'QMatrix':
				say('It requires KC:', map(int, model.Q[question_id]))

			performance = model.predict_performance()
			say('Correct!' if test_data[student_id][question_id] else 'Incorrect.') #, "I expected: %f." % round(performance[question_id], 2))

			replied_so_far.append(question_id)
			results_so_far.append(test_data[student_id][question_id])
			model.estimate_parameters(replied_so_far, results_so_far)
			performance = model.predict_performance()

			say(' '.join(map(lambda x: str(int(10 * round(x, 1))), performance)))
			say('Estimate:', ''.join(map(lambda x: '%d' % int(round(x)), performance)))
			say('   Truth:', ''.join(map(lambda x: '%d' % int(x), test_data[student_id])))

			error_log[-1][t - 1] = evaluate(performance, test_data[student_id], validation_question_set)
			# error_rate[t - 1].append(dummy_count(performance, test_data[student_id], replied_so_far) / (len(performance) - len(replied_so_far)))
			# say('Erreur au tour %d :' % t, error_log[-1][t - 1])


def main():
	files = IO()
	dataset = Dataset(dataset_name, files)
	dataset.load_subset()
	print(dataset)
	step = 1
	for validation_index in dataset.validation_question_sets:
		validation_index = set(validation_index)
		files.update(step)
		for model in models:
			train_power = len(dataset.train_subset)
			error_rate = []
			begin = datetime.now()
			print begin
			log = {}
			prefix = model.get_prefix() + '-%s-%s' % (dataset.nb_questions, train_power)
			train_dataset = [[dataset.data[i][j] for j in dataset.question_subset] for i in dataset.train_subset]
			test_dataset = [[dataset.data[i][j] for j in dataset.question_subset] for i in dataset.test_subset]
			error_log = []
			simulate(model, train_dataset, test_dataset, validation_index, error_log)
			log[model.name] = error_log
			get_results(log, prefix, files)
			files.backup('log-%s-%s-%s' % (dataset_name, prefix, datetime.now().strftime('%d%m%Y%H%M%S')), error_log)
			print datetime.now()
		step += 1

if __name__ == '__main__':
	if sys.argv[1] == 'baseline':
		from baseline import Baseline
		models = [Baseline()]
	elif sys.argv[1] == 'qm':
		from qmatrix import QMatrix
		models = []
		for nb_competences in nb_competences_values:
			models.append(QMatrix(nb_competences=nb_competences))
	elif sys.argv[1] == 'qmspe':
		from qmatrix import QMatrix
		q = QMatrix(nb_competences=8)
		q.load('qmatrix-cdm')
		models = [q]
	elif sys.argv[1] == 'irt':
		from irt import IRT
		models = [IRT()]
	elif sys.argv[1] == 'mirt':
		from mirt import MIRT
		models = [MIRT()]
	elif sys.argv[1] == 'mirtq':
		from mirt import MIRT
		from qmatrix import QMatrix
		q = QMatrix(nb_competences=8)
		# q.load('qmatrix-custom')
		q.load('qmatrix-cdm')
		models = [MIRT(q=q)]
	else:
		from irt import IRT
		models = [IRT(criterion='MEPV')]

	all_student_sampled = True
	models_names = [model.name for model in models]
	main()
