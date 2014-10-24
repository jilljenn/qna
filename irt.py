# coding=utf8
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from calc import logloss
import random

r = robjects.r
ltm = importr('ltm')
cat = importr('catR')

class IRT():
	def __init__(self, Q=None, slip=None, guess=None, prior=None, criterion='MFI'):
		self.name = 'IRT'
		self.criterion = criterion

	def training_step(self, train, opt_Q=True, opt_sg=True):
		nb_students = len(train)
		nb_questions = len(train[0])
		raw_data = map(int, reduce(lambda x, y: x + y, train))
		a = r.matrix(robjects.IntVector(raw_data), nrow=nb_students, byrow=True)
		model = ltm.rasch(a)
		coeff = ltm.coef_rasch(model)
		scores = ltm.factor_scores(model).rx('score.dat')[0].rx('z1')[0]
		r('coeff <- coef(rasch(%s))' % a.r_repr())
		r('one <- rep(1, %d)' % nb_questions)
		r('itembank <- cbind(coeff[,2:1], 1 - one, one)')

	def load(self, filename):
		pass

	def init_test(self):
		r('theta <- 0')

	def next_item(self, replied_so_far, results_so_far):
		next = r('nextItem(itembank, NULL, theta, out = c({}), criterion = "{}")$item'.format(','.join(map(lambda x: str(x + 1), replied_so_far)), self.criterion))[0]
		# nb_questions = r('dim(itembank)[1]')[0]
		# next = random.choice(list(set(range(nb_questions)) - set(replied_so_far)))
		return next - 1

	def estimate_parameters(self, replied_so_far, results_so_far):
		scores_so_far = map(int, results_so_far)
		theta = r('theta <- thetaEst(itembank[c({}),], c({}))'.format(','.join(map(lambda x: str(x + 1), replied_so_far)), ','.join(map(str, scores_so_far))))
		pm = r('semTheta(theta, itembank[c({}),])'.format(','.join(map(str, replied_so_far))))

	def predict_performance(self):
		return tuple(r('round(Pi(theta, itembank)$Pi, 3)'))
