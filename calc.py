# coding=utf-8
import math
from hashlib import md5, sha1


def entr(x):
	return (-1e-16) * math.log(1e-16, 2) if x < 1e-16 else (-x) * math.log(x, 2)

def entropy(l):
	return sum(entr(x) for x in l)

def normalize(p):
	return [x / sum(p) for x in p]

def surround(p):
	return list(map(lambda x: round(x, 3), p))

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

def get_train_checksum(prefix, train):
    return '%s-%s' % (prefix, sha1(train).hexdigest())
    s = prefix
    print(train[0])
    s += ''.join(map(lambda line: ''.join(map(lambda x: str(int(x)), line)), train))
    return md5(s.encode('utf-8')).hexdigest()
