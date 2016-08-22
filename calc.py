# coding=utf-8
import math
import numpy as np


def entr(x):
	return (-1e-16) * math.log(1e-16, 2) if x < 1e-16 else (-x) * math.log(x, 2)

def entropy(l):
	return sum(entr(x) for x in l)

def normalize(p):
	return [x / sum(p) for x in p]

def surround(p):
	return map(lambda x: round(x, 3), p)

def normalize2(p, e):
	return (p * e) / (p * e + (1 - p) * (1 - e))

def entropy1(x):
    return entropy([x, 1 - x])

def entropy_sum(l):
	return sum(map(entropy1, l))

def compute_mean_entropy(p_answering, perf_if_correct, perf_if_incorrect, replied_so_far):
    perf_if_correct_subset = [p for i, p in enumerate(perf_if_correct) if i not in replied_so_far]
    perf_if_incorrect_subset = [p for i, p in enumerate(perf_if_incorrect) if i not in replied_so_far]
    return p_answering * entropy_sum(perf_if_correct_subset) + (1 - p_answering) * entropy_sum(perf_if_incorrect_subset)

def kindlog(x):
	return math.log(1e-16) if x < 1e-16 else math.log(x)

def logloss(estimated, real, only_on_components=[]):
    if len(only_on_components) == 0:
        return 0
    return -sum(kindlog(estimated[i]) if real[i] else kindlog(1 - estimated[i]) for i in range(len(real)) if i in only_on_components) / (len(only_on_components))

def derivative_logloss(estimated, real, coefficients):
    return -sum(coefficients[i] / estimated[i] if real[i] else -coefficients[i] / (1 - estimated[i]) for i in range(len(real))) / len(real)

def avgstd(l):  # Displays mean and variance
    n = len(l)
    mean = float(sum(l)) / n
    var = float(sum(i * i for i in l)) / n - mean * mean
    return round(mean, 3), round(1.96 * math.sqrt(var / n), 3)  # '%.3f ± %.3f' % 

def sample_k(items, L, k, max_nb_iterations=1000, rng=np.random):
    """
    Sample a list of k items from a DPP defined
    by the similarity matrix L. The algorithm
    is iterative and runs for max_nb_iterations.
    The algorithm used is from
    (Fast Determinantal Point Process Sampling withw
    Application to Clustering, Byungkon Kang, NIPS 2013)
    """
    initial = rng.choice(range(len(items)), size=k, replace=False)
    X = [False] * len(items)
    for i in initial:
        X[i] = True
    X = np.array(X)
    for i in range(max_nb_iterations):
        u = rng.choice(np.arange(len(items))[X])
        v = rng.choice(np.arange(len(items))[~X])
        Y = X.copy()
        Y[u] = False
        L_Y = L[Y, :]
        L_Y = L_Y[:, Y]
        L_Y_inv = np.linalg.inv(L_Y)

        c_v = L[v:v+1, :]
        c_v = c_v[:, v:v+1]
        b_v = L[Y, :]
        b_v = b_v[:, v:v+1]
        c_u = L[u:u+1, :]
        c_u = c_u[:, u:u+1]
        b_u = L[Y, :]
        b_u = b_u[:, u:u+1]

        p = min(1, c_v - np.dot(np.dot(b_v.T, L_Y_inv), b_v) /
                (c_u - np.dot(np.dot(b_u.T, L_Y_inv.T), b_u)))
        if rng.uniform() <= p:
            X = Y[:]
            X[v] = True
    return np.array(items)[X]
