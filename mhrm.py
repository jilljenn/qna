import numpy as np
from scipy.stats import norm, multivariate_normal
from my_io import Dataset

REAL = True

if REAL:
    Y = np.array(Dataset('fraction').data)
    N, n = Y.shape
else:
    N = 50
    n = 5
    Y = np.random.randint(2, size=(N, n))

p = 2
c = 1
G = np.zeros((n, p+1, p+1))
SIGMA = c * c * np.eye(p)
NB_ITERATIONS = 50

def add_bias(X):
    N, _ = X.shape
    return np.column_stack((X, np.ones(N)))

def expo(Th, X, sgn=1):
    """
    Th has shape n p+1
    X has shape N p
    """
    X1 = add_bias(X)
    return np.exp(sgn * X1.dot(Th.T))  # Shape N n

def proba1(Th, X):
    exp_minusXT = expo(Th, X, -1)
    return 1 / (1 + exp_minusXT)

def loglikelihood(Th, X):
    exp_XT = expo(Th, X)
    # P = proba1(Th, X)
    # ((1 - Y) * log(1 - P)  # Shape N n
    #     + Y  * log(    P))
    ll = ((Y - 1) * np.log(1 + exp_XT)  # Shape N n
             + Y  * (np.log(exp_XT) - np.log(1 + exp_XT)))
    return ll

def score(Th, X):
    exp_XT = expo(Th, X)
    X1 = add_bias(X)
    C = (Y + (Y - 1) * exp_XT) / (1 + exp_XT)  # Shape N n
    return C.T.dot(X1)  # Shape n p+1

def hessian(Th, X):
    exp_XT = expo(Th, X)
    X1 = add_bias(X)
    XiXiT = np.einsum('ij,ki->ijk', X1, X1.T)  # Shape N p+1 p+1
    Lambda = -exp_XT / (1 + exp_XT) ** 2  # Shape N n
    return np.tensordot(Lambda.T, XiXiT, axes=1)  # Shape n p+1 p+1

def q(xi, xis):
    return multivariate_normal.pdf(xis, mean=xi, cov=SIGMA)

def phi(x):
    return multivariate_normal.pdf(x, mean=np.zeros(p), cov=np.eye(p))

def logacceptance(Th, X):
    # print('hop', loglikelihood(Th, X).sum(axis=1).shape, np.log(phi(X)).shape)
    return loglikelihood(Th, X).sum(axis=1) + np.log(phi(X))

def impute(Th):
    def iterate(X):
        old = logacceptance(Th, X)
        E = np.random.multivariate_normal(mean=np.zeros(p), cov=SIGMA, size=N)
        new = logacceptance(Th, X + E)
        sample = np.random.random(N)
        X += np.diag(np.log(sample) < new - old).dot(E)
        return X
    Xs = [np.zeros((N, p))]
    for _ in range(NB_ITERATIONS):
        Xs.append(iterate(Xs[-1]))
    return Xs[5:]

Th = np.random.random((n, p + 1))
for k in range(1, 100):
    # STEP 1: Imputation
    Xs = impute(Th)
    ll = np.mean([loglikelihood(Th, X).sum() for X in Xs])
    print('Error before', -ll)
    # STEP 2a: Approximation of score
    s = sum([score(Th, X) for X in Xs]) / len(Xs)
    # print(s.shape)
    # STEP 2b: Approximation of hessian
    H = -sum([hessian(Th, X) for X in Xs]) / len(Xs)
    # print(H.shape)
    gamma = 1 / k
    G += gamma * (H - G)
    Ginv = np.stack(np.linalg.inv(G[i, :, :]) for i in range(n))
    # print('Score of norm before', sum(np.linalg.norm(score(Th, X)) for X in Xs) / len(Xs))
    Th += gamma * np.einsum('ijk,ik->ij', Ginv, s)
    # print('Score of norm after', sum(np.linalg.norm(score(Th, X)) for X in Xs) / len(Xs))
    print('Error after', -sum(loglikelihood(Th, X).sum() for X in Xs) / len(Xs))
print(Th)
