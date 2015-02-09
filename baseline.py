# coding=utf8
from calc import surround
import random
import re

class Baseline():
    def __init__(self):
        self.name = 'Baseline'
        self.nb_questions = None
        self.initial_train_responses = []
        self.train_responses = []

    def make_response_vector(self, replied_so_far, results_so_far):
        response_vector = list('.' * self.nb_questions)
        for i in range(len(replied_so_far)):
            response_vector[replied_so_far[i]] = '1' if results_so_far[i] else '0'
        return response_vector

    def training_step(self, train, opt_Q=True, opt_sg=True):
        self.nb_questions = len(train[0])
        for line in train:
            self.initial_train_responses.append(''.join(map(lambda x: str(int(x)), line)))

    def load(self, filename):
        pass

    def init_test(self):
        self.train_responses = self.initial_train_responses[:]

    def next_item(self, replied_so_far, results_so_far):
        response_vector = self.make_response_vector(replied_so_far, results_so_far)
        not_answered = set(range(self.nb_questions)) - set(replied_so_far)
        min_diff = self.nb_questions
        best_q = None
        for q_id in not_answered:
            response_vector[q_id] = '1'
            nb_yes = len(filter(lambda x: re.match(''.join(response_vector), x), self.train_responses))
            response_vector[q_id] = '0'
            nb_no = len(filter(lambda x: re.match(''.join(response_vector), x), self.train_responses))
            response_vector[q_id] = '.'
            if abs(nb_yes - nb_no) < min_diff:
                min_diff = abs(nb_yes - nb_no)
                best_q = q_id
        return q_id

    def estimate_parameters(self, replied_so_far, results_so_far, var_id=''):
        response_vector = self.make_response_vector(replied_so_far, results_so_far)
        self.train_responses = filter(lambda x: re.match(''.join(response_vector), x), self.train_responses)
        print(len(self.train_responses))

    def predict_performance(self, var_id=''):
        proba = [0.] * self.nb_questions
        nb_examples = len(self.train_responses)
        if nb_examples == 0:
            return [0.5] * self.nb_questions
        for response in self.train_responses:
            for i in range(self.nb_questions):
                proba[i] += float(response[i])
        for i in range(self.nb_questions):
            proba[i] /= nb_examples
        # print(self.train_responses)
        # print(surround(proba))
        return proba
