# coding=utf-8
import math

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

def multientropy(l):
	return sum(map(entropy1, l))

def kindlog(x):
	return math.log(1e-16) if x < 1e-16 else math.log(x)

def logloss(estimated, real, replied_so_far=[]):
    if len(real) == len(replied_so_far):
        return 0
    return -sum(kindlog(estimated[i]) if real[i] else kindlog(1 - estimated[i]) for i in range(len(real)) if i not in replied_so_far) / (len(real) - len(replied_so_far))

def derivative_logloss(estimated, real, coefficients):
    return -sum(coefficients[i] / estimated[i] if real[i] else -coefficients[i] / (1 - estimated[i]) for i in range(len(real))) / len(real)

def avgstd(l): # Displays mean and variance
    n = len(l)
    mean = float(sum(l)) / n
    var = float(sum(i * i for i in l)) / n - mean * mean
    return '%.3f ± %.3f' % (round(mean, 3), round(1.96 * math.sqrt(var / n), 3))
