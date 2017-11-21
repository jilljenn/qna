from rpyinterface import RPyInterface
import numpy as np
import random


class Zero(RPyInterface):
	def __init__(self):
		self.name = 'Zero'

	def compute_all_predictions(self):
		return np.array([self.predict_performance() for _ in range(self.nb_students)])

	def training_step(self, train=None):
		pass  # I am lazy

	def init_test(self, validation_question_set):
		pass

	def next_item(self, replied_so_far, results_so_far):
		remaining_questions = set(range(self.nb_questions)) - set(replied_so_far)
		return random.choice(remaining_questions)

	def estimate_parameters(self, replied_so_far, results_so_far):
		pass

	def predict_performance(self):
		return [0.] * self.nb_questions

	def get_prefix(self):
		return 'zero'

	def get_dim(self):
		return 0
