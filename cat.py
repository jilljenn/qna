from datetime import datetime
from calc import logloss, surround
import io
from qmatrix import QMatrix
from irt import IRT

filename = 'sat.light'
n_split = 5
budget = 39
all_student_sampled = True
models = [IRT(), QMatrix()]
models_names = [model.name for model in models]

def display(results):
	for name in results:
		print name, results[name]['mean']

def evaluate(performance, truth, replied_so_far):
	nb_questions = len(performance)
	# print [performance[i] for i in range(nb_questions) if i not in replied_so_far], [truth[i] for i in range(nb_questions) if i not in replied_so_far]
	# return logloss([performance[i] for i in range(nb_questions) if i not in replied_so_far], [truth[i] for i in range(nb_questions) if i not in replied_so_far])
	return logloss(performance, truth)

def get_results(log):
	results = {}
	nb_students = len(log.values()[0])
	for model in models:
		results[model.name] = {'mean': [sum(log[model.name][i][t] for i in range(nb_students)) / nb_students for t in range(budget)]}
	io.backup('stats-%s-%s' % (filename, datetime.now().strftime('%d%m%Y%H%M%S')), results)

def simulate(train_data, test_data, error_log):
	model.training_step(train_data)
	# model.load('qmatrix-19062014141433')
	# model.load('qmatrix-19062014144231')
	nb_students = len(test_data)
	if all_student_sampled:
		student_sample = range(30) #range(nb_students) # All students
	for student_id in student_sample:
		print 'Student', student_id
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
			#print ''.join(map(lambda x: str(int(round(x))), performance))
			#print surround(performance)
			#print ''.join(map(lambda x: str(int(x)), test_data[student_id]))
			error_log[-1][t - 1] = evaluate(performance, test_data[student_id], replied_so_far)
			#print error_log[-1][t - 1]
			"""if t == 38:
				print t, error_log[-1][t]
				print [performance[i] for i in range(len(performance)) if i not in replied_so_far]
				print [test_data[student_id][i] for i in range(len(performance)) if i not in replied_so_far]"""

def main():
	log = {}
	dataset = io.load(filename)['student_data']
	for model in models:
		error_log = []
		simulate(dataset, dataset, error_log)
		log[model.name] = error_log
	get_results(log)
	io.backup('log-%s-%s' % (filename, datetime.now().strftime('%d%m%Y%H%M%S')), error_log)

if __name__ == '__main__':
	main()
