# coding=utf8
from datetime import datetime
from calc import logloss, surround, avgstd
from conf import dataset_name, nb_competences_values
from my_io import IO
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
	return logloss(performance, truth, validation_question_set)

def dummy_count(performance, truth, replied_so_far):
	nb_questions = len(performance)
	# print 'indecision', sum([0.4 <= performance[i] <= 0.6 for i in range(nb_questions) if i not in replied_so_far])
	return sum([(performance[i] < 0.5 and truth[i]) or (performance[i] > 0.5 and not truth[i]) for i in range(nb_questions) if i not in replied_so_far]) # Count errors

def get_results(log, god_prefix, io_handler):
	results = {}
	nb_students = len(log.values()[0])
	budget = len(log.values()[0][0])
	for model_name in log:
		# print model.name
		results[model_name] = {'mean': [avgstd([log[model_name][i][t] for i in range(nb_students)]) for t in range(budget)]}
		"""for t in range(budget):
			print(avgstd(list(log[model.name][i][t] for i in range(nb_students))))"""
	io_handler.backup('stats-%s-%s-%s' % (dataset_name, god_prefix, datetime.now().strftime('%d%m%Y%H%M%S')), results)

def simulate(model, train_data, test_data, validation_question_set, error_log):
	model.training_step(train_data, opt_Q=True, opt_sg=True)
	print(datetime.now())
	print '=' * 10, model.name
	nb_students = len(test_data)
	nb_questions = len(test_data[0])
	budget = nb_questions - len(validation_question_set)
	if all_student_sampled:
		student_sample = range(nb_students) # All students
	error_rate = [[] for _ in range(budget)]
	for student_id in student_sample:
		print 'Étudiant', student_id, test_data[student_id]
		error_log.append([0] * budget)
		model.init_test(validation_question_set=validation_question_set)
		replied_so_far = []
		results_so_far = []
		print 'Estimation initiale :', map(lambda x: round(x, 1), model.predict_performance())
		print 'Erreur initiale :', logloss(model.predict_performance(), test_data[student_id])
		for t in range(1, budget + 1):
			question_id = model.next_item(replied_so_far, results_so_far)
			print
			print 'Tour', t, '-> question', question_id + 1
			if model.name == 'IRT':
				print 'Difficulté :', model.coeff.rx(question_id + 1)[0]
			else:
				print 'Cette question, dans la q-matrice :', map(int, model.Q[question_id])
			replied_so_far.append(question_id)
			results_so_far.append(test_data[student_id][question_id])
			model.estimate_parameters(replied_so_far, results_so_far)
			performance = model.predict_performance()
			print 'Résultat :', 'OK,' if test_data[student_id][question_id] else 'NOK,', "j'avais prévu", round(performance[question_id], 2)
			"""if model.name == 'QMatrix':
				print surround(model.p_test)
				print 'required', [''.join(map(lambda x: str(int(x)), model.Q[i])) for i in range(nb_questions) if i not in replied_so_far]
				print 'slip', [model.slip[i] for i in range(nb_questions) if i not in replied_so_far]
				print 'guess', [model.guess[i] for i in range(nb_questions) if i not in replied_so_far]
				print [surround(performance)[i] for i in range(nb_questions) if i not in replied_so_far]
				print [test_data[student_id][i] for i in range(nb_questions) if i not in replied_so_far]
				print evaluate(performance, test_data[student_id], replied_so_far)"""
			print ' '.join(map(lambda x: str(int(10 * round(x, 1))), performance))
			print 'Estimation :', ''.join(map(lambda x: '%d' % int(round(x)), performance))
			print '    Vérité :', ''.join(map(lambda x: '%d' % int(x), test_data[student_id]))
			error_log[-1][t - 1] = evaluate(performance, test_data[student_id], validation_question_set)
			# error_rate[t - 1].append(dummy_count(performance, test_data[student_id], replied_so_far) / (len(performance) - len(replied_so_far)))
			print 'Erreur au tour %d :' % t, error_log[-1][t - 1]
			"""if t == 38:
				print t, error_log[-1][t]
				print [performance[i] for i in range(len(performance)) if i not in replied_so_far]
				print [test_data[student_id][i] for i in range(len(performance)) if i not in replied_so_far]"""
	"""for t in range(budget):
		print error_rate[t]
		print avgstd(error_rate[t])"""

def main():
	io_handle = IO()
	full_dataset = io_handle.load(dataset_name, prefix='data')['student_data']#[::-1]
	if dataset_name == 'sat':
		nb_questions = 20
		test_power = 80
		# question_subset = range(nb_questions)[:20]
		j = json.load(open('subset.json'))
		question_subset = j['question_subset']
		train_subset = j['train_subset']
		test_subset = sorted(set(range(296)) - set(train_subset))
		# question_subset = [2 * i for i in range(nb_questions)] # sorted(random.sample(range(len(full_dataset[0])), nb_questions))
	elif dataset_name == 'fraction':
		nb_questions = 20
		test_power = 100
		# question_subset = range(nb_questions)
		j = json.load(open('subset.json'))
		question_subset = j['question_subset']
		validation_question_sets = j['validation_question_sets']
		train_subset = j['train_subset']
		test_subset = sorted(set(range(536)) - set(train_subset))
	elif dataset_name == 'castor6e':
		nb_questions = 17
		test_power = 10000
		question_subset = range(nb_questions)
		j = json.load(open('subset.json'))
		question_subset = j['question_subset']
		train_subset = j['train_subset']
		test_subset = sorted(set(range(58939)) - set(train_subset))
	elif dataset_name.startswith('3x2'):
		nb_questions = 3
		test_power = 10
		question_subset = range(nb_questions)
	elif dataset_name == 'functional-analysis':
		nb_questions = 21
		test_power = 487
		question_subset = range(nb_questions)
		j = json.load(open('subset.json'))
		question_subset = j['question_subset']
		train_subset = j['train_subset']
		test_subset = sorted(set(range(2287)) - set(train_subset))
	elif dataset_name == 'moodle':
		nb_questions = 15
		test_power = 550
		question_subset = range(nb_questions)
		j = json.load(open('subset.json'))
		question_subset = j['question_subset']
		train_subset = j['train_subset']
		test_subset = sorted(set(range(2350)) - set(train_subset))
	step = 1
	for validation_index in validation_question_sets:
		validation_index = set(validation_index)
		io_handle.update(step)
		for model in models:
			error_rate = []
			train_power = len(full_dataset) - test_power
			begin = datetime.now()
			print begin
			log = {}
			if model.name == 'QMatrix':
				god_prefix = '%s-%s-%s' % (model.nb_competences if sys.argv[1] == 'qm' else '888', nb_questions, train_power)
			elif model.name == 'Baseline':
				god_prefix = 'baseline-%s-%s' % (nb_questions, train_power)
			elif model.criterion == 'MFI':
				god_prefix = 'irt-%s-%s' % (nb_questions, train_power)
			else:
				god_prefix = 'mepv-irt-%s-%s' % (nb_questions, train_power)
			dataset = [[full_dataset[i][j] for j in question_subset] for i in range(len(full_dataset))]
			train_dataset = dataset[:train_power]
			test_dataset = dataset[-test_power:]
			train_dataset = [dataset[i] for i in train_subset]
			test_dataset = [dataset[i] for i in test_subset]
			error_log = []
			simulate(model, train_dataset, test_dataset, validation_index, error_log)
			print god_prefix
			log[model.name] = error_log
			get_results(log, god_prefix, io_handle)
			io_handle.backup('log-%s-%s-%s' % (dataset_name, god_prefix, datetime.now().strftime('%d%m%Y%H%M%S')), error_log)
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
	else:
		from irt import IRT
		models = [IRT(criterion='MEPV')]

	# n_split = 5
	# budget = 20
	all_student_sampled = True
	models_names = [model.name for model in models]
	main()
