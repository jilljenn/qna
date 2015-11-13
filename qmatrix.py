# coding=utf8
import random
from calc import logloss, derivative_logloss, normalize, entropy, compute_mean_entropy, surround
from itertools import product
import my_io
from datetime import datetime
from operator import mul

# state (over 2^K) => comp (over K) where K = nb_competences

def bool2int(l):
	return int(''.join(map(str, map(int, l))), 2)

def prod(l):
	if len(list(l)) == 0:
		return 1
	return reduce(mul, l)

DEFAULT_SLIP = 1e-3
DEFAULT_GUESS = 1e-3
K = 3
LOOP_TIMEOUT = 20
SLIP_GUESS_PRECISION = 1e-4
ALPHA = 1e-4

class QMatrix():
	def __init__(self, nb_competences=K, Q=None, slip=None, guess=None, prior=None):
		self.name = 'QMatrix'
		self.nb_competences = nb_competences
		self.Q = Q
		self.prior = prior if prior else [0.5] * nb_competences
		self.p_states = None
		self.p_test = None
		self.slip = slip
		self.guess = guess
		self.error = None
		self.from_expert = False
		self.validation_question_set = None

	def load(self, filename):
		data = my_io.load(filename)
		self.Q = data['Q']
		self.nb_competences = len(self.Q[0])  # Do not forget!
		self.slip = data['slip']
		self.guess = data['guess']
		self.p_states = data['p_states']
		self.from_expert = True
		# self.prior = data['prior'] # TODO

	def save(self, filename):
		my_io.backup(filename, {'Q': self.Q, 'slip': self.slip, 'guess': self.guess, 'prior': self.prior, 'error': self.error, 'p_states': self.p_states})

	def match(self, question, state):
		return bool2int(question) & ((1 << self.nb_competences) - 1 - state) == 0

	def training_step(self, train, opt_Q=True, opt_sg=True, timeout=LOOP_TIMEOUT):
		nb_students = len(train)
		nb_questions = len(train[0])
		if not self.Q:
			self.Q = [[random.randint(1, 2) == 2 for _ in range(self.nb_competences)] for _ in range(nb_questions)]
		if not self.slip:
			self.slip = [DEFAULT_SLIP] * nb_questions
		if not self.guess:
			self.guess = [DEFAULT_GUESS] * nb_questions
		loop = 0
		self.display_qmatrix()
		self.infer_state(train)
		while not self.from_expert and loop < timeout: # TODO
			# print 'Infer state %d' % loop
			self.infer_state(train)
			#print self.model_error(train)
			if opt_Q:
				#print 'Infer Q-Matrix FAST %d' % loop
				self.infer_qmatrix_fast(train)
				#print self.model_error(train)
			if opt_sg:
				#print 'Infer guess/slip %d' % loop
				# pass
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
		self.display_qmatrix()
		if timeout is None:
			self.generate_student_data(50)
		self.save('qmatrix-%s' % datetime.now().strftime('%d%m%Y%H%M%S'))

	def display_qmatrix(self):
		for i, line in enumerate(self.Q):
			print(''.join(map(lambda x: str(int(x)), line)), self.guess[i], self.slip[i])

	def init_test(self, validation_question_set):
		self.p_test = self.prior
		self.validation_question_set = validation_question_set

	def compute_proba_question(self, question_id, p_competences, mode=None):
		proba = prod([p for comp, p in enumerate(p_competences) if self.Q[question_id][comp]])
		if not mode:
			return proba * (1 - self.slip[question_id]) + (1 - proba) * self.guess[question_id]
		elif mode == 'slip':
			return -self.slip[question_id] * proba
		else:
			return self.guess[question_id] * (1 - proba)

	def product(self, p_competences, state):
		return prod([p if (state >> (self.nb_competences - 1 - comp)) & 1 == 1 else 1 - p for comp, p in enumerate(p_competences)])

	def predict_future(self, question_id, p_competences):
		proba_question = self.compute_proba_question(question_id, p_competences)
		# print 'comp', p_competences
		# debug_vector = [self.product(p_competences, state) for state in range(1 << self.nb_competences)]
		# debug_vector_if_correct = normalize([p * (1 - self.slip[question_id]) if self.match(self.Q[question_id], state) else p * self.guess[question_id] for state, p in enumerate(debug_vector)])
		# debug_vector_if_incorrect = normalize([p * self.slip[question_id] if self.match(self.Q[question_id], state) else p * (1 - self.guess[question_id]) for comp, p in enumerate(debug_vector)])
		# print 'debug', debug_vector
		proba = prod([p for comp, p in enumerate(p_competences) if self.Q[question_id][comp]])
		not_proba_question = proba * self.slip[question_id] + (1 - self.guess[question_id]) * (1 - proba)
		# print '=' * 10, (not_proba_question + proba_question == 1)
		future_if_correct = p_competences[:]
		future_if_incorrect = p_competences[:]
		# print 'question asked', self.Q[question_id]
		for comp, p in enumerate(p_competences):
			if self.Q[question_id][comp]:
				future_if_correct[comp] = (proba * (1. - self.slip[question_id]) + self.guess[question_id] * (1. - (1. - p) - proba)) / proba_question
				future_if_incorrect[comp] = (proba * self.slip[question_id] + (1. - self.guess[question_id]) * (1. - (1. - p) - proba)) / not_proba_question
				if future_if_correct[comp] > 1:
					future_if_correct[comp] = 1.
					print 'oops1'
				if future_if_correct[comp] <= 0:
					future_if_correct[comp] = 0.
					print 'oops2'
				if future_if_incorrect[comp] > 1:
					future_if_incorrect[comp] = 1.
					print 'oops3'
				if future_if_incorrect[comp] <= 0:
					future_if_incorrect[comp] = 0.
					print 'oops4'
		# print 'future obtained', future_if_incorrect
		# print(debug_vector_if_correct)
		# new_p_competences = [sum(debug_vector_if_incorrect[state] for state in range(1 << self.nb_competences) if (state >> (self.nb_competences - 1 - comp)) & 1 == 1) for comp in range(self.nb_competences)]
		# print 'we should have obtained', new_p_competences
		# print 'which would lead to', [self.product(new_p_competences, state) for state in range(1 << self.nb_competences)]
		assert all(0 <= p <= 1 for p in future_if_correct) and all(0 <= p <= 1 for p in future_if_incorrect)  # CAUTION
		return future_if_incorrect, future_if_correct

	def ask_question(self, question_id, is_correct_answer, p_competences):
		return self.predict_future(question_id, p_competences)[is_correct_answer] # Wooo

	def estimate_parameters(self, replied_so_far, results_so_far):
		p = self.ask_question(replied_so_far[-1], results_so_far[-1], self.p_test)
		print 'Inférence des compétences du candidat :', map(lambda x: round(x, 2), p)
		self.p_test = p

	def infer_state(self, train):
		nb_students = len(train)
		nb_questions = len(train[0])
		self.p_states = []
		for student_id in range(nb_students):
			self.p_states.append(self.prior[:])
			for question_id in range(nb_questions): # Ask her ALL questions!
				self.p_states[student_id] = self.ask_question(question_id, train[student_id][question_id], self.p_states[student_id])
			# print 'student', student_id, self.p_states[student_id]

	def evaluate_error(self, question_id, train, coefficients=None, sg=None):
		nb_students = len(train)
		# print "niveaux, sachant qu'on s'intéresse à la question", question_id
		"""for line in self.p_states:
			print(surround(line))"""
		estimated_column = [self.compute_proba_question(question_id, self.p_states[student_id]) for student_id in range(nb_students)]
		real_column = [train[student_id][question_id] for student_id in range(nb_students)]
		# print(surround(estimated_column), real_column)
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
				a, b = 0., 0.15#1.#0.5#1#.#0.3#1. #0.2 # Limite
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
					#if question_id in [1, 2]:
					#	print question_id, question_error, self.model_error(train)
					#	print error_min, line
					error_min = question_error
					best_line = line
			"""if question_id < 10:
				print 'new matrix'
				for i in range(question_id):
					print(self.Q[i], self.slip[i], self.guess[i])"""
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
					# print error_min, self.Q[question_id]
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
		max_info = None
		best_question = None
		for question_id in set(range(nb_questions)) - self.validation_question_set:
			if question_id in replied_so_far:
				continue
			p_answering = self.compute_proba_question(question_id, self.p_test)
			# future_if_incorrect, future_if_correct = self.predict_future(question_id, self.p_test)
			# mean_entropy = p_answering * entropy(future_if_correct) + (1 - p_answering) * entropy(future_if_incorrect)
			# mean_entropy = compute_mean_entropy(p_answering, self.predict_performance(future_if_incorrect), self.predict_performance(future_if_correct), replied_so_far + [question_id])
			info = p_answering * (1 - p_answering)
			#if not min_entropy or mean_entropy < min_entropy:
			if not max_info or info > max_info:
				#min_entropy = mean_entropy
				max_info = info
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
