import math

def entr(x):
	return x if x < 1e-6 else (-x) * math.log(x, 2)

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

def logloss(estimated, real):
	return -sum(math.log(estimated[i]) if real[i] else math.log(1 - estimated[i]) for i in range(len(real))) / len(real)		

def derivative_logloss(estimated, real, coefficients):
	return -sum(coefficients[i] / estimated[i] if real[i] else -coefficients[i] / (1 - estimated[i]) for i in range(len(real))) / len(real)
