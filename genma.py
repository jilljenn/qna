import numpy as np
import math
import random
from sklearn.linear_model import LogisticRegression


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class GenMA:
    def __init__(self, dim=8):
        self.name = 'GenMA'
        self.dim = dim

    def load(self):
        U, V, bias = np.load('genma.npy')
        self.U = U
        self.V = V
        self.bias = bias

    def compute_all_errors(self, dataset):
        self.load()
        user_train = dataset.train_subsets[0]
        train = np.array(dataset.data)[user_train]
        pred = sigmoid(self.U.dot(self.V.T) + self.bias)[user_train]
        print('Train RMSE:', np.mean((pred - train) ** 2) ** 0.5)
        print('Train NLL:', -np.mean(np.log(np.abs(pred - train))))
        print('Train accuracy:', np.mean(np.round(pred) == train))

    def training_step(self, train_data):
        self.load()
        self.nb_questions = len(train_data[0])

    def init_test(self, validation_question_set=[]):
        self.theta = np.random.random(self.dim)

    def next_item(self, replied_so_far, results_so_far):
        return random.choice(range(self.nb_questions))

    def estimate_parameters(self, replied_so_far, results_so_far, var_id=''):
        if len(set(results_so_far)) == 2:
            clf = LogisticRegression()
            clf.fit(self.V[replied_so_far], results_so_far)
            self.theta = clf.coef_[0]
        elif results_so_far[0] == True:
            self.theta = np.array([0.] * self.dim)
        else:
            self.theta = np.array([0.] * self.dim)

    def predict_performance(self, var_id=''):
        return sigmoid(self.theta.dot(self.V.T) + self.bias).tolist()

    def get_prefix(self):
        return 'genma'

    def get_dim(self):
        return self.dim
