import numpy as np
import math
import random
from sklearn.linear_model import LogisticRegression


def sigmoid(x):
    return 1 / (1 + math.exp(-x))

class GenMA:
    def __init__(self, dim=8):
        self.name = 'GenMA'
        self.dim = dim

    def training_step(self, train_data):
        U, V, bias = np.load('genma.npy')
        self.V = V
        self.bias = bias[:, 0]
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
            self.theta += 1
        else:
            self.theta -= 1

    def predict_performance(self, var_id=''):
        return list(map(sigmoid, self.theta.dot(self.V.T) + self.bias))

    def get_prefix(self):
        return 'genma'

    def get_dim(self):
        return self.dim
