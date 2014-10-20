from datetime import datetime
from calc import logloss, surround, avgstd
import my_io, random
from qmatrix import QMatrix
#from irt import IRT

filename = 'castor6e' # 17
n_split = 5
# budget = 20
all_student_sampled = True
models = []
for nb_competences in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
	models.append(QMatrix(nb_competences=nb_competences))
#models = [IRT()]
#models = [IRT(criterion='MEPV')]
models_names = [model.name for model in models]

def display(results):
	for name in results:
		print name, results[name]['mean']

def evaluate(performance, truth, replied_so_far):
	nb_questions = len(performance)
	# print [performance[i] for i in range(nb_questions) if i not in replied_so_far], [truth[i] for i in range(nb_questions) if i not in replied_so_far]
	# return logloss([performance[i] for i in range(nb_questions) if i not in replied_so_far], [truth[i] for i in range(nb_questions) if i not in replied_so_far])
	return logloss(performance, truth)

def dummy_count(performance, truth, replied_so_far):
	nb_questions = len(performance)
	# print 'indecision', sum([0.4 <= performance[i] <= 0.6 for i in range(nb_questions) if i not in replied_so_far])
	return sum([(performance[i] < 0.5 and truth[i]) or (performance[i] > 0.5 and not truth[i]) for i in range(nb_questions) if i not in replied_so_far]) # Count errors

def get_results(log, god_prefix):
	results = {}
	nb_students = len(log.values()[0])
	budget = len(log.values()[0][0])
	for model in models:
		results[model.name] = {'mean': [sum(log[model.name][i][t] for i in range(nb_students)) / nb_students for t in range(budget)]}
	my_io.backup('stats-%s-%s-%s' % (filename, god_prefix, datetime.now().strftime('%d%m%Y%H%M%S')), results)

def simulate(model, train_data, test_data, error_log):
	model.training_step(train_data)
	nb_students = len(test_data)
	nb_questions = len(test_data[0])
	budget = nb_questions - 1
	if all_student_sampled:
		student_sample = range(nb_students) # All students
	error_rate = [[] for _ in range(budget)]
	for student_id in student_sample:
		#print 'Student', student_id
		error_log.append([0] * budget)
		model.init_test()
		replied_so_far = []
		results_so_far = []
		for t in range(1, budget + 1):
			#print 'Turn', t
			question_id = model.next_item(replied_so_far, results_so_far)
			replied_so_far.append(question_id)
			results_so_far.append(test_data[student_id][question_id])
			model.estimate_parameters(replied_so_far, results_so_far)
			performance = model.predict_performance()
			#print surround(performance)
			#print ''.join(map(lambda x: str(int(round(x))), performance))
			#print ''.join(map(lambda x: str(int(x)), test_data[student_id]))
			error_log[-1][t - 1] = evaluate(performance, test_data[student_id], replied_so_far)
			error_rate[t - 1].append(dummy_count(performance, test_data[student_id], replied_so_far) / (len(performance) - len(replied_so_far)))
			#print error_log[-1][t - 1]
			"""if t == 38:
				print t, error_log[-1][t]
				print [performance[i] for i in range(len(performance)) if i not in replied_so_far]
				print [test_data[student_id][i] for i in range(len(performance)) if i not in replied_so_far]"""
	for t in range(budget):
		print error_rate[t]
		print avgstd(error_rate[t])

def main():
	full_dataset = my_io.load(filename, prefix='data')['student_data'][::-1]
	# nb_questions = 20
	if filename == 'sat':
		question_subset = [2 * i for i in range(20)] # sorted(random.sample(range(len(full_dataset[0])), nb_questions))
	else:
		nb_questions = 17
		question_subset = range(nb_questions)
	for model in models:
		error_rate = []
		for nb_questions in [17]: # , 30, 40
			for test_power in [10000]: # , 40, 160
				train_power = len(full_dataset) - test_power
				begin = datetime.now()
				log = {}
				if model.name == 'QMatrix':
					god_prefix = '%s-%s-%s' % (model.nb_competences, nb_questions, train_power)
				elif model.criterion == 'MFI':
					god_prefix = 'irt-%s-%s' % (nb_questions, train_power)
				else:
					god_prefix = 'mepv-irt-%s-%s' % (nb_questions, train_power)
				dataset = [[full_dataset[i][j] for j in question_subset] for i in range(len(full_dataset))]
				error_log = []
				simulate(model, dataset[:train_power], dataset[-test_power:], error_log)
				print god_prefix
				log[model.name] = error_log
				get_results(log, god_prefix)
				my_io.backup('log-%s-%s-%s' % (filename, god_prefix, datetime.now().strftime('%d%m%Y%H%M%S')), error_log)
				print datetime.now() - begin

if __name__ == '__main__':
	main()
