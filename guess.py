# coding=utf8
import math, random
from scipy.stats import beta
import numpy as np
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

nb_questions = 20
nb_objects = 50

Q = [[[random.randint(1, 10) for _ in range(2)] for _ in range(nb_objects)] for _ in range(nb_questions)] # Q[i][j][0-1] pour les valeurs α-β de la question j sachant que l'objet est i
Qt = [[float(Q[i][j][1]) / (Q[i][j][0] + Q[i][j][1]) for j in range(nb_objects)] for i in range(nb_questions)] # Q[i][j] vaut l'espérance de la variable, c'est-à-dire p(Q_j = 1|X = i)

myQ = [[[1, 1] for _ in range(nb_objects)] for _ in range(nb_questions)]

print np.array(Qt)

p = [random.random() for _ in range(nb_objects)]
p = [x / sum(p) for x in p] # A priori

guessed_object = random.choice(range(nb_objects))

entropies = []
curve = [[] for _ in range(nb_objects)]
c = 0
while entropy(p) > 0.1:
	print c, entropy(p)
	dH = np.array(map(entropy1, np.squeeze(np.asarray(np.matrix(Qt).dot(p)))) - np.matrix([map(entropy1, q) for q in Qt]).dot(p)) # H(E(Q_j)) - E(H(Q_j)) pour chaque Q_j
	dH = list(np.array(dH).reshape(-1,))
	best_dh, best_j = max([(dh, j) for j, dh in enumerate(dH)])
	answer = random.random() < Qt[best_j][guessed_object]
	p = normalize([q * (Qt[best_j][i] if answer else 1 - Qt[best_j][i]) for i, q in enumerate(p)])
	# print c, surround(p), 'j\'ai posé', best_j, 'on m\'a répondu', answer, entropy(p), dH
	entropies.append(entropy(p))
	for i in range(nb_objects):
		curve[i].append(p[i])
	c += 1

print guessed_object

fig, ax = plt.subplots()
ax.plot(entropies, color='purple')
for i in range(nb_objects):
	ax.plot(curve[i])
# ax.plot(curve[guessed_object])
ax.set_title('TMTC')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])
plt.show()
