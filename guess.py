import math, random
from scipy.stats import beta
import numpy as np

def entropy(l):
	return sum(- p * math.log(p, 2) for p in l)

def entropy1(x):
	return entropy([x, 1 - x])

nb_questions = 10
nb_objects = 5

Q = [[[random.randint(1, 10) for _ in range(2)] for _ in range(nb_objects)] for _ in range(nb_questions)] # Q[i][j][0-1] pour les valeurs α-β de la question j sachant que l'objet est i
Qt = [[float(Q[i][j][1]) / (Q[i][j][0] + Q[i][j][1]) for j in range(nb_objects)] for i in range(nb_questions)] # Q[i][j] vaut l'espérance de la variable, c'est-à-dire p(Q_j = 1|X = i)

p = [random.random() for _ in range(nb_objects)]
p = [x / sum(p) for x in p] # A priori

print map(entropy1, np.squeeze(np.asarray(np.matrix(Qt).dot(p)))) - np.matrix([map(entropy1, q) for q in Qt]).dot(p) # H(E(Q_j)) - E(H(Q_j)) pour chaque Q_j
