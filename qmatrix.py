# coding=utf8
import math, random
from scipy.stats import beta
import numpy as np
from numpy.random import beta
import matplotlib.pyplot as plt
from operator import mul, and_, or_
import json

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

nb_questions = 10
nb_competences = 4
nb_states = 1 << nb_competences
eps = 0.1

# Q[i][j] pour les valeurs α-β de la question j sachant que l'objet est i
Q = [[random.randint(1, 2) == 1 for _ in range(nb_competences)] for _ in range(nb_questions)]

true_competences = random.choice(range(nb_states))
p_competences = [1. / nb_states] * nb_states

print match([True, False, False], 0)
pass

print 'Véritables compétences', bin(true_competences)[2:]
for _ in range(10):
	min_entropy = entropy(p_competences)
	best_question = -1
	for i in range(nb_questions):
		p_answering = sum([p for state, p in enumerate(p_competences) if match(Q[i], state)])
		my_competences_if_correct = normalize([p * (1 - eps) if match(Q[i], state) else p * eps for state, p in enumerate(p_competences)])
		my_competences_if_incorrect = normalize([p * eps if match(Q[i], state) else p * (1 - eps) for state, p in enumerate(p_competences)])
		mean_entropy = p_answering * entropy(my_competences_if_correct) + (1 - p_answering) * entropy(my_competences_if_incorrect)
		if mean_entropy < min_entropy:
			min_entropy = mean_entropy
			best_question = i
	print 'On lui pose la question', best_question, Q[best_question], min_entropy
	if match(Q[best_question], true_competences):
		print 'OK'
		p_competences = normalize([p * (1 - eps) if match(Q[best_question], state) else p * eps for state, p in enumerate(p_competences)])
	else:
		print 'NOK'
		p_competences = normalize([p * eps if match(Q[best_question], state) else p * (1 - eps) for state, p in enumerate(p_competences)])
	print map(lambda (x, y): (bin(x)[2:], y), enumerate(surround(p_competences)))

"""myQ = [[[1, 1] for _ in range(nb_competences)] for _ in range(nb_questions)]
p = [1. / nb_competences] * nb_competences
# print np.squeeze(np.asarray(np.matrix(Qt).dot(p)))
dH = np.array(map(entropy1, np.squeeze(np.asarray(np.matrix(Qt).dot(p)))) - np.matrix([map(entropy1, q) for q in Qt]).dot(p))
dH = list(np.array(dH).reshape(-1,))
indexes = {}
for i in range(nb_questions):
	indexes[dH[i]] = i
Q2 = []
for ent in sorted(dH)[::-1]:
	Q2.append(Q[indexes[ent]])
Qt = [[float(Q2[i][j][1]) / (Q2[i][j][0] + Q2[i][j][1]) for j in range(nb_competences)] for i in range(nb_questions)]
dH = np.array(map(entropy1, np.squeeze(np.asarray(np.matrix(Qt).dot(p)))) - np.matrix([map(entropy1, q) for q in Qt]).dot(p))
dH = list(np.array(dH).reshape(-1,))
for ent in dH:
	print ent

# p = [random.random() for _ in range(nb_competences)]
# p = [x / sum(p) for x in p] # A priori

# thought_object = random.choice(range(nb_competences))

entropies = []
curve = [[] for _ in range(nb_competences)]
nb_losses = 0
nb_wins = 0
for k in range(2):
	print k
	for thought_object in range(nb_competences):
		print thought_object
		history = []
		p = [1. / nb_competences] * nb_competences
		for _ in range(10): # 20Q
			myQt = [[float(myQ[i][j][1]) / (myQ[i][j][0] + myQ[i][j][1]) for j in range(nb_competences)] for i in range(nb_questions)]
			dH_bundle = [[] for _ in range(nb_questions)]
			for _ in range(100):
				Qt_tmp = [[beta(myQ[i][j][0], myQ[i][j][1]) for j in range(nb_competences)] for i in range(nb_questions)]
				dH = np.array(map(entropy1, np.squeeze(np.asarray(np.matrix(Qt_tmp).dot(p)))) - np.matrix([map(entropy1, q) for q in Qt_tmp]).dot(p)) # H(E(Q_j)) - E(H(Q_j)) pour chaque Q_j
				dH = list(np.array(dH).reshape(-1,))
				for i in range(nb_questions):
					dH_bundle[i].append(dH[i])
			for i in range(nb_questions):
				dH[i] = sorted(dH_bundle[i])[-5] # On conserve le 5e meilleur pour UCB
			best_dh, best_j = max([(dh, j) for j, dh in enumerate(dH)])
			# print 'Je choisis la question %d' % best_j
			answer = random.random() < Qt[best_j][thought_object]
			history.append((best_j, answer))
			p = normalize([q * (myQt[best_j][i] if answer else 1 - myQt[best_j][i]) for i, q in enumerate(p)])
			# print c, surround(p), 'j\'ai posé', best_j, 'on m\'a répondu', answer, entropy(p), dH
			entropies.append(entropy(p))
			for i in range(nb_competences):
				curve[i].append(p[i])
		_, guessed_object = max((p[i], i) for i in range(nb_competences))
		if guessed_object == thought_object:
			print 'WIN', k
			nb_wins += 1
		else:
			nb_losses += 1
		for question, answer in history:
			myQ[question][thought_object][answer] += 1
p = [1. / nb_competences] * nb_competences
# print np.squeeze(np.asarray(np.matrix(Qt).dot(p)))
dH = np.array(map(entropy1, np.squeeze(np.asarray(np.matrix(Qt).dot(p)))) - np.matrix([map(entropy1, q) for q in Qt]).dot(p))
dH = list(np.array(dH).reshape(-1,))
for i in range(nb_questions):
	for j in range(nb_competences):
		print '%d-%d (%f)' % (myQ[i][j][0], myQ[i][j][1], Qt[i][j]),
	print dH[i]
for i in range(nb_questions):
	print i, ':', sum(map(sum, myQ[i]))
np.save(open('the_matrix.npy', 'w'), myQ)

print guessed_object, p[guessed_object]

fig, ax = plt.subplots()
ax.plot(entropies, color='purple')
for i in range(nb_competences):
	ax.plot(curve[i])
# ax.plot(curve[guessed_object])
ax.set_title('TMTC')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])
plt.show()
"""