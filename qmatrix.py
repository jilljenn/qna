# coding=utf8
import random
from calc import logloss, derivative_logloss, normalize, entropy
from itertools import product
import io

def bool2int(l):
	return int(''.join(map(str, map(int, l))), 2)

DEFAULT_SLIP = 0.2
DEFAULT_GUESS = 0.2
K = 6
LOOP_TIMEOUT = 10
SLIP_GUESS_PRECISION = 1e-2

class QMatrix():
	def __init__(self, nb_competences=K, Q=None, slip=None, guess=None, prior=None):
		self.name = 'QMatrix'
		self.nb_competences = nb_competences
		self.Q = Q
		self.prior = prior if prior else [1 / 1 << nb_competences] * (1 << nb_competences)
		self.p_states = None
		self.p_test = None
		self.slip = slip
		self.guess = guess

	def load(self, filename):
		data = io.load(filename)
		self.Q = data['Q']
		self.slip = data['slip']
		self.guess = data['guess']
		# self.prior = data['prior']

	def save(self, filename):
		io.backup('stuff', {'Q': self.Q, 'slip': self.slip, 'guess': self.guess, 'prior': self.prior})

	def match(self, question, state):
		return bool2int(question) & ((1 << self.nb_competences) - 1 - state) == 0

	def training_step(self, train, opt_Q=True, opt_sg=True, timeout=LOOP_TIMEOUT):
		nb_students = len(train)
		nb_questions = len(train[0])
		if not self.Q:
			self.Q = [[random.randint(1, 2) == 1 for _ in range(self.nb_competences)] for _ in range(nb_questions)]
		if not self.slip:
			self.slip = [DEFAULT_SLIP] * nb_questions
		if not self.guess:
			self.guess = [DEFAULT_GUESS] * nb_questions
		loop_limit = 0
		while loop_limit < timeout: # TODO
			self.infer_state(train)
			if opt_sg:
				self.infer_guess_slip(train)
			if opt_Q:
				self.infer_qmatrix(train)
			self.infer_prior()
			print self.model_error(train)
			loop_limit += 1

	def init_test(self):
		self.p_test = self.prior

	def compute_proba_question(self, question_id, p_competences, mode=None):
		proba = sum(p for state, p in enumerate(p_competences) if self.match(self.Q[question_id], state))
		if not mode:
			return proba * (1 - self.slip[question_id]) + (1 - proba) * self.guess[question_id]
		elif mode == 'slip':
			return -self.slip[question_id] * proba
		else:
			return self.guess[question_id] * (1 - proba)

	def predict_future(self, question_id, p_competences):
		future_if_correct = normalize([p * (1 - self.slip[question_id]) if self.match(self.Q[question_id], state) else p * self.guess[question_id] for state, p in enumerate(p_competences)])
		future_if_incorrect = normalize([p * self.slip[question_id] if self.match(self.Q[question_id], state) else p * (1 - self.guess[question_id]) for state, p in enumerate(p_competences)])
		return future_if_incorrect, future_if_correct

	def ask_question(self, question_id, is_correct_answer, p_competences):
		return self.predict_future(question_id, p_competences)[is_correct_answer] # Wooo

	def estimate_parameters(self, replied_so_far, results_so_far):
		self.p_test = self.ask_question(replied_so_far[-1], results_so_far[-1], self.p_test)

	def infer_state(self, train):
		nb_students = len(train)
		nb_questions = len(train[0])
		self.p_states = []
		for student_id in range(nb_students):
			self.p_states.append(self.prior[:])
			for question_id in range(nb_questions): # Ask her ALL questions!
				self.p_states[student_id] = self.ask_question(question_id, train[student_id][question_id], self.p_states[student_id])

	def evaluate_error(self, question_id, train, coefficients=None, sg=None):
		nb_students = len(train)
		estimated_column = [self.compute_proba_question(question_id, self.p_states[student_id]) for student_id in range(nb_students)]
		real_column = [train[student_id][question_id] for student_id in range(nb_students)]
		if coefficients:
			return derivative_logloss(estimated_column, real_column, coefficients) - 0.05 * (1 / sg - 1 / (1 - sg)) # Ahem
		else:
			return logloss(estimated_column, real_column)

	def model_error(self, train):
		nb_questions = len(self.Q)
		return sum(self.evaluate_error(question_id, train) for question_id in range(nb_questions)) / nb_questions

	def infer_guess_slip(self, train):
		nb_students = len(train)
		nb_questions = len(self.Q)
		for question_id in range(nb_questions):
			for mode in ['slip', 'guess']:
				a, b = 0., 1.
				while b - a > SLIP_GUESS_PRECISION:
					sg = (a + b) / 2
					coefficients = [self.compute_proba_question(question_id, self.p_states[student_id], mode=mode) for student_id in range(nb_students)]
					derivative = self.evaluate_error(question_id, train, coefficients=coefficients, sg=sg)
					if derivative > 0:
						b = sg
					else:
						a = sg
				if mode == 'slip':
					self.slip[question_id] = (a + b) / 2
				else:
					self.guess[question_id] = (a + b) / 2

	def infer_qmatrix(self, train):
		nb_questions = len(self.Q)
		for question_id in range(nb_questions):
			error_min = None
			for line in product([True, False], repeat=self.nb_competences):
				self.Q[question_id] = line
				question_error = self.evaluate_error(question_id, train)
				if not error_min or question_error < error_min:
					error_min = question_error
					best_line = line
			self.Q[i] = best_line

	def infer_prior(self):
		nb_students = len(self.p_states)
		nb_states = len(self.p_states[0])
		self.prior = [sum(self.p_states[student_id][j] for student_id in range(nb_students)) / nb_students for j in range(nb_states)]

	def next_item(self, replied_so_far, results_so_far):
		nb_questions = len(self.Q)
		min_entropy = None
		best_question = None
		for question_id in range(nb_questions):
			if question_id in replied_so_far:
				continue
			p_answering = self.compute_proba_question(question_id, self.p_test)
			future_if_incorrect, future_if_correct = self.predict_future(question_id, self.p_test)
			mean_entropy = p_answering * entropy(future_if_correct) + (1 - p_answering) * entropy(future_if_incorrect)
			if not min_entropy or mean_entropy < min_entropy:
				min_entropy = mean_entropy
				best_question = question_id
		return best_question

	def predict_performance(self):
		nb_questions = len(self.Q)
		return [self.compute_proba_question(question_id, self.p_test) for question_id in range(nb_questions)]

	def generate_student_data(self, nb_students):
		nb_questions = len(self.Q)
		states = sorted(random.choice(range(1 << self.nb_competences)) for _ in range(nb_students)) # Generate random states
		student_data = [[] for _ in range(nb_students)]
		for student_id in range(nb_students):
			for question_id in range(nb_questions):
				is_skilled = self.match(self.Q[question_id], states[student_id])
				student_data[student_id].append((is_skilled and random.random() > self.slip[question_id]) or (not is_skilled and random.random() <= self.guess[question_id]))
		return student_data
