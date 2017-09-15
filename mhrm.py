import numpy as np
from scipy.stats import norm, multivariate_normal

N = 5
n = 10
p = 2
c = 1
SIGMA = c * c * np.eye(p)
Y = np.random.randint(2, size=(N, n))
NB_ITERATIONS = 5

def proba1(Th, X):
    return 1 / (1 + np.exp(-np.column_stack((X, np.ones(N)))
                              .dot(Th.T)))

def loglikelihood(Th, X):
    return ((1 - Y) * (1 - proba1(Th, X))
               + Y  *      proba1(Th, X))

def score(Th, X):
    pass

def hessian(Th, X):
    pass

def q(xi, xis):
    return multivariate_normal.pdf(xis, mean=xi, cov=SIGMA)

def phi(x):
    return multivariate_normal.pdf(x, mean=np.zeros(p), cov=np.eye(p))

def acceptance(Th, X):
    return np.prod(likelihood(Th, X), axis=1) * phi(X)

def impute(Th):
    def iterate(X):
        old = acceptance(Th, X)
        E = np.random.multivariate_normal(mean=np.zeros(p), cov=SIGMA, size=N)
        new = acceptance(Th, X + E)
        sample = np.random.random(N)
        X += np.diag(sample < new / old).dot(E)
        return X
    X = np.zeros((N, p))
    for _ in range(NB_ITERATIONS):
        X = iterate(X)
    return X

Th = np.random.random((n, p + 1))
X = impute(Th)
print(X)
