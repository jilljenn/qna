# coding=utf8
import random
from calc import logloss, derivative_logloss, normalize, entropy, compute_mean_entropy
from itertools import product
import my_io
from datetime import datetime

def bool2int(l):
	return int(''.join(map(str, map(int, l))), 2)

DEFAULT_SLIP = 0.2
DEFAULT_GUESS = 0.2
K = 3
LOOP_TIMEOUT = 10
SLIP_GUESS_PRECISION = 1e-2
ALPHA = 0.#2e-6

class QMatrix():
	def __init__(self, nb_competences=K, Q=None, slip=None, guess=None, prior=None):
		self.name = 'QMatrix'
		self.nb_competences = nb_competences
		self.Q = Q
		self.prior = prior if prior else [1. / (1 << nb_competences)] * (1 << nb_competences)
		self.p_states = None
		self.p_test = None
		self.slip = slip
		self.guess = guess
		self.error = None

	def load(self, filename):
		data = my_io.load(filename)
		self.Q = data['Q']
		self.slip = data['slip']
		self.guess = data['guess']
		self.p_states = data['p_states']
		# self.prior = data['prior'] # TODO

	def save(self, filename):
		my_io.backup(filename, {'Q': self.Q, 'slip': self.slip, 'guess': self.guess, 'prior': self.prior, 'error': self.error, 'p_states': self.p_states})

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
		loop = 0
		self.infer_state(train)
		while loop < timeout: # TODO
			# print 'Infer state %d' % loop
			self.infer_state(train)
			#print self.model_error(train)
			if opt_Q:
				#print 'Infer Q-Matrix FAST %d' % loop
				self.infer_qmatrix(train)
				#print self.model_error(train)
			if opt_sg:
				#print 'Infer guess/slip %d' % loop
				self.infer_guess_slip(train)
				#print self.model_error(train)
			#print 'Infer prior %d' % loop
			print self.model_error(train)
			self.infer_prior()
			loop += 1
		"""print 'Q-matrice', self.Q
		print self.guess
		print self.slip
		print '->', self.model_error(train)"""
		self.model_error(train)
		if timeout == 0:
			self.generate_student_data(50)
		self.save('qmatrix-%s' % datetime.now().strftime('%d%m%Y%H%M%S'))

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
			return derivative_logloss(estimated_column, real_column, coefficients) - ALPHA * (1 / sg - 1 / (1 - sg)) # Ahem
		else:
			return logloss(estimated_column, real_column)

	def model_error(self, train):
		nb_questions = len(self.Q)
		self.error = sum(self.evaluate_error(question_id, train) for question_id in range(nb_questions)) / nb_questions
		return self.error

	def infer_guess_slip(self, train):
		nb_students = len(train)
		nb_questions = len(self.Q)
		for question_id in range(nb_questions):
			for mode in ['slip', 'guess']:
				# if mode == 'guess':
					# print('was', self.guess[question_id], self.model_error(train))
				a, b = 0., 1.
				while b - a > SLIP_GUESS_PRECISION:
					sg = (a + b) / 2
					if mode == 'slip':
						self.slip[question_id] = sg
					else:
						self.guess[question_id] = sg
						# print('test', sg, self.model_error(train))
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
					# print('will', (a + b) / 2, self.model_error(train))
				# print(self.model_error(train))

	def infer_qmatrix(self, train):
		nb_questions = len(self.Q)
		for question_id in range(nb_questions):
			error_min = self.evaluate_error(question_id, train)
			best_line = self.Q[question_id]
			for line in product([True, False], repeat=self.nb_competences):
				self.Q[question_id] = line
				question_error = self.evaluate_error(question_id, train)
				if question_error < error_min:
					# print question_id, question_error, self.model_error(train)
					# print error_min, line
					error_min = question_error
					best_line = line
			self.Q[question_id] = best_line # Put back the best (we once forgot to do so)

	def infer_qmatrix_fast(self, train):
		nb_questions = len(self.Q)
		for question_id in range(nb_questions):
			error_min = self.evaluate_error(question_id, train)
			best_line = self.Q[question_id]
			for competence in range(self.nb_competences):
				self.Q[question_id][competence] = not self.Q[question_id][competence] # Flip
				question_error = self.evaluate_error(question_id, train)
				if question_error < error_min:
					# print question_id, question_error, self.model_error(train)
					# print error_min, line
					error_min = question_error
				else:
					self.Q[question_id][competence] = not self.Q[question_id][competence] # Backflip
			# self.Q[question_id] = best_line

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
			# mean_entropy = p_answering * entropy(future_if_correct) + (1 - p_answering) * entropy(future_if_incorrect)
			mean_entropy = compute_mean_entropy(p_answering, self.predict_performance(future_if_incorrect), self.predict_performance(future_if_correct), replied_so_far + [question_id])
			if not min_entropy or mean_entropy < min_entropy:
				min_entropy = mean_entropy
				best_question = question_id
		return best_question

	def predict_performance(self, p_states=None):
		nb_questions = len(self.Q)
		if not p_states:
			p_states = self.p_test
		return [self.compute_proba_question(question_id, p_states) for question_id in range(nb_questions)]

	def generate_student_data(self, nb_students, state_prior):
		nb_questions = len(self.Q)
		states = []
		for _ in range(nb_students):
			random_competence_vector = ['1' if random.random() < state_prior[i] else '0' for i in range(self.nb_competences)] # Generate random state
			states.append(int(''.join(random_competence_vector), 2))
		student_data = [[] for _ in range(nb_students)]
		for student_id in range(nb_students):
			for question_id in range(nb_questions):
				is_skilled = self.match(self.Q[question_id], states[student_id])
				student_data[student_id].append((is_skilled and random.random() > self.slip[question_id]) or (not is_skilled and random.random() <= self.guess[question_id]))
		my_io.backup('fake_data', {'student_data': student_data})
		# return student_data
