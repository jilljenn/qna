from datetime import datetime
from calc import logloss, surround
import io, random
from qmatrix import QMatrix
#from irt import IRT

filename = 'sat'
n_split = 5
# budget = 20
all_student_sampled = True
models = [QMatrix()]
models_names = [model.name for model in models]

def display(results):
	for name in results:
		print name, results[name]['mean']

def evaluate(performance, truth, replied_so_far):
	nb_questions = len(performance)
	# print [performance[i] for i in range(nb_questions) if i not in replied_so_far], [truth[i] for i in range(nb_questions) if i not in replied_so_far]
	# return logloss([performance[i] for i in range(nb_questions) if i not in replied_so_far], [truth[i] for i in range(nb_questions) if i not in replied_so_far])
	return logloss(performance, truth)

def get_results(log, god_prefix):
	results = {}
	nb_students = len(log.values()[0])
	budget = len(log.values()[0][0])
	for model in models:
		results[model.name] = {'mean': [sum(log[model.name][i][t] for i in range(nb_students)) / nb_students for t in range(budget)]}
	io.backup('stats-%s-%s-%s' % (filename, god_prefix, datetime.now().strftime('%d%m%Y%H%M%S')), results)

def simulate(model, train_data, test_data, error_log):
	model.training_step(train_data)
	nb_students = len(test_data)
	nb_questions = len(test_data[0])
	budget = nb_questions - 1
	if all_student_sampled:
		student_sample = range(nb_students) # All students
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
			#print error_log[-1][t - 1]
			"""if t == 38:
				print t, error_log[-1][t]
				print [performance[i] for i in range(len(performance)) if i not in replied_so_far]
				print [test_data[student_id][i] for i in range(len(performance)) if i not in replied_so_far]"""

def main():
	full_dataset = io.load(filename, prefix='data')['student_data'][::-1]
	for nb_competences in [4, 5, 6, 7, 8, 9, 10]:
		for nb_questions in [20]: # , 30, 40
			for train_power in [80]: # , 40, 160
				log = {}
				god_prefix = '%s-%s-%s' % (nb_competences, nb_questions, train_power)
				model = QMatrix(nb_competences=nb_competences)
				#god_prefix = 'irt-%s-%s' % (nb_questions, train_power)
				#model = IRT()
				question_subset = sorted(random.sample(range(len(full_dataset[0])), nb_questions))
				dataset = [[full_dataset[i][j] for j in question_subset] for i in range(len(full_dataset))]
				error_log = []
				simulate(model, dataset[:train_power], dataset[160:], error_log)
				print god_prefix
				log[model.name] = error_log
				get_results(log, god_prefix)
				io.backup('log-%s-%s-%s' % (filename, god_prefix, datetime.now().strftime('%d%m%Y%H%M%S')), error_log)

if __name__ == '__main__':
	main()
