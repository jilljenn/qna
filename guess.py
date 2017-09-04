# coding=utf8
import math, random
from scipy.stats import beta
import numpy as np
from numpy.random import beta
import matplotlib.pyplot as plt

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

nb_questions = 10
nb_objects = 1 << 5

# Q[i][j][0-1] pour les valeurs α-β de la question j sachant que l'objet est i
Q = [[[random.randint(1, 10) for _ in range(2)] for _ in range(nb_objects)] for _ in range(nb_questions)]
Q[-1] = [(0, 1)] * (nb_objects / 2) + [(1, 1)] * (nb_objects / 2)
Q[-2] = [(0, 1)] * (nb_objects / 2) + [(1, 0)] * (nb_objects / 2)
Q[-3] = [(1, 1)] * nb_objects
# Q[i][j] vaut l'espérance de la variable, c'est-à-dire p(Q_j = 1|X = i)
Qt = [[float(Q[i][j][1]) / (Q[i][j][0] + Q[i][j][1]) for j in range(nb_objects)] for i in range(nb_questions)]
print Qt[-1], Qt[-2]
myQ = [[[1, 1] for _ in range(nb_objects)] for _ in range(nb_questions)]
p = [1. / nb_objects] * nb_objects
# print np.squeeze(np.asarray(np.matrix(Qt).dot(p)))
dH = np.array(map(entropy1, np.squeeze(np.asarray(np.matrix(Qt).dot(p)))) - np.matrix([map(entropy1, q) for q in Qt]).dot(p))
dH = list(np.array(dH).reshape(-1,))
indexes = {}
for i in range(nb_questions):
	indexes[dH[i]] = i
Q2 = []
for ent in sorted(dH)[::-1]:
	Q2.append(Q[indexes[ent]])
Qt = [[float(Q2[i][j][1]) / (Q2[i][j][0] + Q2[i][j][1]) for j in range(nb_objects)] for i in range(nb_questions)]
dH = np.array(map(entropy1, np.squeeze(np.asarray(np.matrix(Qt).dot(p)))) - np.matrix([map(entropy1, q) for q in Qt]).dot(p))
dH = list(np.array(dH).reshape(-1,))
for ent in dH:
	print ent

# p = [random.random() for _ in range(nb_objects)]
# p = [x / sum(p) for x in p] # A priori

# thought_object = random.choice(range(nb_objects))

entropies = []
curve = [[] for _ in range(nb_objects)]
nb_losses = 0
nb_wins = 0
for k in range(2):
	print k
	for thought_object in range(nb_objects):
		print thought_object
		history = []
		p = [1. / nb_objects] * nb_objects
		for _ in range(10): # 20Q
			myQt = [[float(myQ[i][j][1]) / (myQ[i][j][0] + myQ[i][j][1]) for j in range(nb_objects)] for i in range(nb_questions)]
			dH_bundle = [[] for _ in range(nb_questions)]
			for _ in range(100):
				Qt_tmp = [[beta(myQ[i][j][0], myQ[i][j][1]) for j in range(nb_objects)] for i in range(nb_questions)]
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
			for i in range(nb_objects):
				curve[i].append(p[i])
		_, guessed_object = max((p[i], i) for i in range(nb_objects))
		if guessed_object == thought_object:
			print 'WIN', k
			nb_wins += 1
		else:
			nb_losses += 1
		for question, answer in history:
			myQ[question][thought_object][answer] += 1
p = [1. / nb_objects] * nb_objects
# print np.squeeze(np.asarray(np.matrix(Qt).dot(p)))
dH = np.array(map(entropy1, np.squeeze(np.asarray(np.matrix(Qt).dot(p)))) - np.matrix([map(entropy1, q) for q in Qt]).dot(p))
dH = list(np.array(dH).reshape(-1,))
for i in range(nb_questions):
	for j in range(nb_objects):
		print '%d-%d (%f)' % (myQ[i][j][0], myQ[i][j][1], Qt[i][j]),
	print dH[i]
for i in range(nb_questions):
	print i, ':', sum(map(sum, myQ[i]))
np.save(open('the_matrix.npy', 'w'), myQ)

"""print guessed_object, p[guessed_object]

fig, ax = plt.subplots()
ax.plot(entropies, color='purple')
for i in range(nb_objects):
	ax.plot(curve[i])
# ax.plot(curve[guessed_object])
ax.set_title('TMTC')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])
plt.show()
"""