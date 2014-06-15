# coding=utf8
import math, random
import numpy as np
from numpy.random import beta
from operator import mul, and_, or_
import json
from itertools import product

SIMULATED = 0
REAL = 1

mode = REAL
nb_questions = 10
nb_competences = 5
nb_states = 1 << nb_competences
guess = [0.1] * nb_questions
slip = [0.1] * nb_questions
budget = 20
nb_students = 10

def entr(x):
	return x if x < 1e-6 else (-x) * math.log(x, 2)

def entropy(l):
	return sum(entr(x) for x in l)

def entropy1(x):
	return entropy([x, 1 - x])

def normalize(p):
	return [x / sum(p) for x in p]

def surround(p):
	return map(lambda x: round(x, 3), p)

def normalize2(p, e):
	return (p * e) / (p * e + (1 - p) * (1 - e))

def multientropy(l):
	return sum(map(entropy1, l))

def bool2int(l):
	return int(''.join(map(str, map(int, l))), 2)

def match(question, state):
	return bool2int(question) & (nb_states - 1 - state) == 0

def backup(filename, data):
	with open(filename, 'w') as f:
		f.write(json.dumps(data))

def generate(silent=False):
	states = sorted(random.choice(range(nb_states)) for _ in range(nb_students))
	Q = [[random.randint(1, 2) == 1 for _ in range(nb_competences)] for _ in range(nb_questions)]
	"""print('\n# True q-matrix\n')
	for line in Q:
		print(line)"""
	if silent:
		return Q
	"""else:
		states = sorted(random.sample(range(nb_states), nb_students))
		Q = []
		for _ in range(2):
			Q.append([True] * nb_competences)
		Q.extend([k >= i / 2 for k in range(nb_competences)] for i in range(4, 12))"""
	if not silent:
		student_data = [[] for _ in range(nb_students)]
		print('\n# True student data\n')
		for i in range(nb_students):
			for j in range(nb_questions):
				is_skilled = match(Q[j], states[i])
				student_data[i].append((is_skilled and random.random() > slip[j]) or (not is_skilled and random.random() <= guess[j]))
			#print student_data[i], states[i]
		backup('stuff.json', {'states': states, 'Q': Q, 'student_data': student_data, 'slip': slip, 'guess': guess})
	# export_to_guacamole(student_data)

def export_to_guacamole(student_data):
	with open('qmatrix.data', 'w') as f:
		for i, student in enumerate(student_data):
			for j in range(nb_questions):
				f.write(','.join(map(str, [i, j, 1, student_data[i][j]])) + '\n')

def ask_question(student_id, question_id, p_competences, Q, slip, guess):
	s = slip[question_id]
	g = guess[question_id]
	if student_data[student_id][question_id]:
		return normalize([p * (1 - s) if match(Q[question_id], state) else p * g for state, p in enumerate(p_competences)])
	else:
		return normalize([p * s if match(Q[question_id], state) else p * (1 - g) for state, p in enumerate(p_competences)])

def sq(x):
	return x*x

def logloss(estimated, real):
	return -sum(math.log(estimated[i]) if real[i] else math.log(1 - estimated[i]) for i in range(len(real))) / len(real)

def qmatrix_logloss(Q, slip, guess, p_states=None):
	if not p_states:
		p_states = infer_state(Q, slip, guess)
	"""for line in p_states:
		print surround(line)"""
	dat_logloss = 0
	for i in range(nb_questions):
		estimated_column = [compute_proba_question(p_states[student_id], i, Q, slip[i], guess[i]) for student_id in range(nb_students)]
		# print p_states[0], slip[i], guess[i]
		real_column = [student_data[student_id][i] for student_id in range(nb_students)]
		tmp = logloss(estimated_column, real_column)
		"""if i == 0:
			print 'total', i, surround(p_states[-1]), tmp, surround(estimated_column), Q[i]
			print 'total, esti', estimated_column
			print 'total, real', real_column"""
		"""if i == 1:
			print i, surround(p_states[-1]), tmp, surround(estimated_column), Q[i]"""
		dat_logloss += tmp
		# print dat_logloss
	return dat_logloss / nb_questions

def compute_proba_question(p_competences, question_id, Q, s, g):
	proba = 0
	for state, p in enumerate(p_competences):
		if match(Q[question_id], state):
			proba += p
	return proba * (1 - s) + (1 - proba) * g

def infer_state(Q, slip, guess):
	p_states = []
	# print('\nDistribution of probability\n')
	for i in range(nb_students):
		p_states.append([1. / nb_states] * nb_states)
		for j in range(nb_questions):
			p_states[i] = ask_question(i, j, p_states[i], Q, slip, guess)
		# print(surround(p_states[i]))
	return p_states

def infer_guess_slip(p_states):
	for i in range(nb_questions):
		logloss_min = 100000
		g = 0.1
		for s in np.arange(0.1, 1, 0.1):
			estimated_column = [compute_proba_question(p_states[student_id], i, Q, s, g) for student_id in range(nb_students)] 
			real_column = [student_data[student_id][i] for student_id in range(nb_students)]
			if s == 0.1:
				pass
				# print('hey', estimated_column, real_column, logloss(estimated_column, real_column))
			temp = logloss(estimated_column, real_column) + (s-0.1)*(s-0.1)*0
			# print temp, estimated_column, real_column
			if temp < logloss_min:
				# print('mieux', estimated_column, real_column, logloss(estimated_column, real_column))
				logloss_min = temp
				slip[i] = s
		logloss_min = 100000
		s = slip[i]
		for g in np.arange(0.1, 1, 0.1):
			estimated_column = [compute_proba_question(p_states[student_id], i, Q, s, g) for student_id in range(nb_students)]
			real_column = [student_data[student_id][i] for student_id in range(nb_students)]
			temp = logloss(estimated_column, real_column) + (g-0.1)*(g-0.1)*0
			if temp < logloss_min:
				logloss_min = temp
				guess[i] = g

def infer_qmatrix(p_states, true_Q):
	for i in range(nb_questions):
		logloss_min = 100000
		for line in product([True, False], repeat=nb_competences):
			if i == 0:
				temp_total = qmatrix_logloss(Q, slip, guess, p_states)
			Q[i] = line
			estimated_column = [compute_proba_question(p_states[student_id], i, Q, slip[i], guess[i]) for student_id in range(nb_students)]
			real_column = [student_data[student_id][i] for student_id in range(nb_students)]
			temp = logloss(estimated_column, real_column)
			if temp < logloss_min:
				"""if i == 0:
					print
					print 'un pas', logloss_min, temp, logloss_min - temp, 'n_question', i
					#print 'esti', estimated_column
					#print 'real', real_column
					print"""
				logloss_min = temp
				best_line = line
				Q[i] = best_line
				# print 'totale', temp_total - qmatrix_logloss(Q, slip, guess, p_states)
		Q[i] = best_line
		# print([true_Q[i][j] == Q[i][j] for j in range(nb_competences)], 0, true_Q[i], 0, Q[i], slip[i], guess[i], logloss_min)

def train(true_Q):
	"""I like trains."""
	previous_v = -1
	temp = -2
	while previous_v != temp:
		#print(_)
		# temp = str(qmatrix_logloss(Q, slip, guess)) + " "
		p_states = infer_state(Q, slip, guess)
		#temp = str(qmatrix_logloss(Q, slip, guess, p_states)) + " "
		infer_guess_slip(p_states)
		#temp += str(qmatrix_logloss(Q, slip, guess, p_states)) + " "
		infer_qmatrix(p_states, true_Q)
		#temp += str(qmatrix_logloss(Q, slip, guess, p_states)) + " "
		#print temp
		previous_v = temp
		temp = qmatrix_logloss(Q, slip, guess)
	# print temp
	backup('data/result.json', {'p_states': p_states, 'guess': guess, 'slip': slip, 'Q': Q})
	#print
	return p_states

# generate()

# Q[i][j] pour les valeurs α-β de la question j sachant que l'objet est i
# Q = [[random.randint(1, 2) == 1 for _ in range(nb_competences)] for _ in range(nb_questions)]
if mode == SIMULATED:
	stuff = json.load(open('stuff.json'))
	student_data = stuff['student_data']
	states = stuff['states']
	true_Q = stuff['Q']
	true_slip = stuff['slip']
	true_guess = stuff['guess']
	Q = generate(silent=True)
	guess = [0.05] * nb_questions
	slip = [0.05] * nb_questions
	p_states = train(true_Q)
	print "True value : " + str(qmatrix_logloss(true_Q, true_guess, true_slip)) + "\n"
	print qmatrix_logloss(Q, slip, guess)
else:
	sat = json.load(open('data/sat.json'))
	student_data = sat['student_data']
	nb_questions = len(student_data[0])
	nb_students = len(student_data)

# print true_Q

"""
for i in range(1):
	Q = generate(silent=True)
	guess = [0.05] * nb_questions
	slip = [0.05] * nb_questions
	p_states = train(true_Q if mode == SIMULATED else Q)
"""

result = json.load(open('data/sat-qmatrix.json'))
Q = result['Q']
guess = result['guess']
slip = result['slip']

# print true_Q

loglosses = [[0] * budget for _ in range(nb_students)]
student_sample = range(nb_students)
for student_id in student_sample: #range(nb_students):
	replied_so_far = []
	# true_competences = states[student_id] # random.choice(range(nb_states)) # Gars médian
	p_competences = [1. / nb_states] * nb_states
	# print 'Véritables compétences', bin(true_competences)[2:]
	for t in range(budget):
		min_entropy = entropy(p_competences)
		best_question = -1
		for i in range(nb_questions):
			if i in replied_so_far: # On ne repose pas les questions déjà posées
				continue
			# p_answering = sum([p for state, p in enumerate(p_competences) if match(Q[i], state)])
			p_answering = compute_proba_question(p_competences, i, Q, guess[i], slip[i])
			my_competences_if_correct = normalize([p * (1 - slip[i]) if match(Q[i], state) else p * guess[i] for state, p in enumerate(p_competences)])
			my_competences_if_incorrect = normalize([p * slip[i] if match(Q[i], state) else p * (1 - guess[i]) for state, p in enumerate(p_competences)])
			mean_entropy = p_answering * entropy(my_competences_if_correct) + (1 - p_answering) * entropy(my_competences_if_incorrect)
			if mean_entropy < min_entropy:
				min_entropy = mean_entropy
				best_question = i
		# print 'Tour', t + 1, ': on lui pose la question', best_question, Q[best_question], min_entropy
		p_competences = ask_question(student_id, best_question, p_competences, Q, slip, guess)
		replied_so_far.append(best_question)
		# print sorted(map(lambda (x, y): (y, bin(x)[2:]), enumerate(surround(p_competences))))[::-1][:5]
		proba_question = [0] * nb_questions
		for i in range(nb_questions):
			proba_question[i] = compute_proba_question(p_competences, i, Q, slip[i], guess[i])
		# print surround(proba_question)
		# print 'Résultats / vrais résultats'
		# print ''.join(map(lambda x: str(int(round(x))), proba_question))
		# print ''.join(map(lambda x: str(int(x)), student_data[student_id]))
		loglosses[student_id][t] = logloss(proba_question, student_data[student_id])
		# print loglosses[student_id][t]

loglosses_mean = [sum(loglosses[i][t] for i in student_sample) / len(student_sample) for t in range(budget)]
# print loglosses_mean

backup('data/logloss-qmatrix-all.json', loglosses)
