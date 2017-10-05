import numpy as np
from scipy.stats import norm, multivariate_normal
from rpyinterface import RPyInterface
from my_io import Dataset

# REAL = True

# if REAL:
#     Y = np.array(Dataset('fraction').data)
#     N, n = Y.shape
# else:
#     N = 50
#     n = 5
#     Y = np.random.randint(2, size=(N, n))


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

def loglikelihood(Th, X, Y):
    exp_XT = expo(Th, X)
    # P = proba1(Th, X)
    # ((1 - Y) * log(1 - P)  # Shape N n
    #     + Y  * log(    P))
    ll = ((Y - 1) * np.log(1 + exp_XT)  # Shape N n
             + Y  * (np.log(exp_XT) - np.log(1 + exp_XT)))
    return ll

def score(Th, X, Y):
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


class MHRM(RPyInterface):
    def __init__(self, dim, nb_iterations=100, nb_samples=50, nb_burned=5):
        c = 1  # Mean standard error of Gaussian prior
        self.name = 'MHRM'
        self.nb_iterations = nb_iterations
        self.nb_samples = nb_samples
        self.nb_burned = nb_burned
        self.dim = dim
        self.p = dim
        self.SIGMA = c * c * np.eye(self.p)
        self.N = None  # Number of students
        self.n = None  # Number of questions
        self.G = None  # Approximation of Hessian
        self.data = None  # Training data

    # def q(xi, xis):
    #     return multivariate_normal.pdf(xis, mean=xi, cov=self.SIGMA)

    def phi(self, x):
        return multivariate_normal.pdf(x, mean=np.zeros(self.p), cov=np.eye(self.p))

    def logacceptance(self, Th, X):
        # print('hop', loglikelihood(Th, X).sum(axis=1).shape, np.log(phi(X)).shape)
        return loglikelihood(Th, X, self.data).sum(axis=1) + np.log(self.phi(X))

    def impute(self, Th):
        def iterate(X):
            old = self.logacceptance(Th, X)
            E = np.random.multivariate_normal(mean=np.zeros(self.p), cov=self.SIGMA, size=self.N)
            new = self.logacceptance(Th, X + E)
            sample = np.random.random(self.N)
            X += np.diag(np.log(sample) < new - old).dot(E)
            return X
        Xs = [np.zeros((self.N, self.p))]
        for _ in range(self.nb_samples):
            Xs.append(iterate(Xs[-1]))
        return Xs[self.nb_burned:]

    def compute_all_predictions(self):
        Xs = self.impute(self.Th)
        X = sum(X for X in Xs) / len(Xs)
        p = proba1(self.Th, X)
        return p

    def compute_all_errors(self):
        Xs = self.impute(self.Th)
        X = sum(X for X in Xs) / len(Xs)
        p = proba1(self.Th, X)
        print('Train RMSE:', ((p - self.data) ** 2).mean() ** 0.5)
        print('Train NLL:', -np.log(1 - abs(p - self.data)).mean())
        print('Train accuracy:', (np.round(p) == self.data).mean())

    def training_step(self, train):
        self.data = np.array(train)
        self.N, self.n = self.data.shape
        G = np.zeros((self.n, self.p + 1, self.p + 1))
        Th = np.random.random((self.n, self.p + 1))
        for k in range(1, self.nb_iterations):
            # STEP 1: Imputation
            Xs = self.impute(Th)
            ll = np.mean([loglikelihood(Th, X, self.data).sum() for X in Xs])
            print('Error before', -ll)
            # STEP 2a: Approximation of score
            s = sum([score(Th, X, self.data) for X in Xs]) / len(Xs)
            # print(s.shape)
            # STEP 2b: Approximation of hessian
            H = -sum([hessian(Th, X) for X in Xs]) / len(Xs)
            # print(H.shape)
            gamma = 1 / k
            G += gamma * (H - G)
            Ginv = np.stack(np.linalg.inv(G[i, :, :]) for i in range(self.n))
            # print('Score of norm before', sum(np.linalg.norm(score(Th, X)) for X in Xs) / len(Xs))
            Th += gamma * np.einsum('ijk,ik->ij', Ginv, s)
            # print('Score of norm after', sum(np.linalg.norm(score(Th, X)) for X in Xs) / len(Xs))
            print('Error after', -sum(loglikelihood(Th, X, self.data).sum() for X in Xs) / len(Xs))
        self.Th = Th
        self.compute_all_errors()
        return Th

    def get_prefix(self):
        return 'mhrm'

    def get_dim(self):
        return self.dim

    def predict_performance(self):
        pass

'''Train RMSE: 0.328045644763
Train NLL: 0.344868054709
Train accuracy: 0.850477326969'''