import math, random
from scipy.stats import beta
import numpy as np

def entropy(l):
	return sum(- p * math.log(p, 2) for p in l)

def entropy1(x):
	return entropy([x, 1 - x])

nb_questions = 10
nb_answers = 5

Q = [[[random.randint(1, 10) for _ in range(2)] for _ in range(nb_answers)] for _ in range(nb_questions)]
Qt = [[float(Q[i][j][1]) / (Q[i][j][0] + Q[i][j][1]) for j in range(nb_answers)] for i in range(nb_questions)]

p = [random.random() for _ in range(nb_answers)]
p = [x / sum(p) for x in p]

print map(entropy1, np.squeeze(np.asarray(np.matrix(Qt).dot(p)))) - np.matrix([map(entropy1, q) for q in Qt]).dot(p) # H(E(Q)) - E(H(Q))
