# coding=utf8
import math, random
from scipy.stats import beta
import numpy as np
from numpy.random import beta
import matplotlib.pyplot as plt
from operator import mul, and_, or_
import json

RANDOM = 0

mode = RANDOM
nb_questions = 100
nb_competences = 6
nb_states = 1 << nb_competences
guess = 0.1
slip = 0.1
budget = 20

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

def generate(nb_students):
	if mode == RANDOM:
		states = sorted(random.choice(range(nb_states)) for _ in range(nb_students))
		Q = [[random.randint(1, 2) == 1 for _ in range(nb_competences)] for _ in range(nb_questions)]
	else:
		states = sorted(random.sample(range(nb_states), nb_students))
		Q = []
		for _ in range(2):
			Q.append([True] * nb_competences)
		Q.extend([k >= i / 2 for k in range(nb_competences)] for i in range(4, 12))
	student_data = [[] for _ in range(nb_students)]
	for i in range(nb_students):
		for j in range(nb_questions):
			student_data[i].append(match(Q[j], states[i]))
	open('stuff.json', 'w').write(json.dumps({'states': states, 'Q': Q, 'student_data': student_data}))
	# export_to_guacamole(student_data)

def export_to_guacamole(student_data):
	with open('qmatrix.data', 'w') as f:
		for i, student in enumerate(student_data):
			for j in range(nb_questions):
				f.write(','.join(map(str, [i, j, 1, student_data[i][j]])) + '\n')

def logloss(estimated, real):
	return sum(math.log(estimated[i]) if real[i] else math.log(1 - estimated[i]) for i in range(len(real))) / len(real)

generate(100)

# Q[i][j] pour les valeurs α-β de la question j sachant que l'objet est i
# Q = [[random.randint(1, 2) == 1 for _ in range(nb_competences)] for _ in range(nb_questions)]
stuff = json.load(open('stuff.json'))
states = stuff['states']
Q = stuff['Q']
student_data = stuff['student_data']

true_competences = states[len(states) / 2] # random.choice(range(nb_states)) # Gars médian
p_competences = [1. / nb_states] * nb_states

print 'Véritables compétences', bin(true_competences)[2:]
loglosses = []
for t in range(budget):
	min_entropy = entropy(p_competences)
	best_question = -1
	for i in range(nb_questions):
		p_answering = sum([p for state, p in enumerate(p_competences) if match(Q[i], state)])
		my_competences_if_correct = normalize([p * (1 - slip) if match(Q[i], state) else p * guess for state, p in enumerate(p_competences)])
		my_competences_if_incorrect = normalize([p * slip if match(Q[i], state) else p * (1 - guess) for state, p in enumerate(p_competences)])
		mean_entropy = p_answering * entropy(my_competences_if_correct) + (1 - p_answering) * entropy(my_competences_if_incorrect)
		if mean_entropy < min_entropy:
			min_entropy = mean_entropy
			best_question = i
	print 'Tour', t + 1, ': on lui pose la question', best_question, Q[best_question], min_entropy
	is_skilled = match(Q[best_question], true_competences)
	if (is_skilled and random.random() > slip) or (not is_skilled and random.random() <= guess):
		print 'OK'
		p_competences = normalize([p * (1 - slip) if match(Q[best_question], state) else p * guess for state, p in enumerate(p_competences)])
	else:
		print 'NOK'
		p_competences = normalize([p * slip if match(Q[best_question], state) else p * (1 - guess) for state, p in enumerate(p_competences)])
	print sorted(map(lambda (x, y): (y, bin(x)[2:]), enumerate(surround(p_competences))))[::-1][:5]
	proba_question = [0] * nb_questions
	for i in range(nb_questions):
		for state, p in enumerate(p_competences):
			if match(Q[i], state):
				proba_question[i] += p
		proba_question[i] = proba_question[i] * (1 - slip) + (1 - proba_question[i]) * guess

	print surround(proba_question)
	print 'Résultats / vrais résultats'
	print ''.join(map(lambda x: str(int(round(x))), proba_question))
	print ''.join(map(lambda x: str(int(x)), student_data[len(states) / 2]))
	loglosses.append(logloss(proba_question, student_data[len(states) / 2]))
	print loglosses[-1]

fig, ax = plt.subplots()
ax.plot(range(len(loglosses)), map(math.exp, loglosses), color='blue')
ax.set_title('Log loss')
plt.show()
