# coding=utf8
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import random, json
import math
r = robjects.r
ltm = importr('ltm')
cat = importr('catR')
student_data = json.load(open('stuff.json'))['student_data']
raw_data = reduce(lambda x, y: x + y, student_data)
a = r.matrix(robjects.IntVector(raw_data), nrow=len(student_data), byrow=True)
model = ltm.rasch(a)
coeff = ltm.coef_rasch(model)
scores = ltm.factor_scores(model).rx('score.dat')[0].rx('z1')[0]
# print tuple(scores)[len(student_data) / 2]

def logloss(estimated, real):
	return sum(math.log(estimated[i]) if real[i] else math.log(1 - estimated[i]) for i in range(len(real))) / len(real)

r('coeff <- coef(rasch(%s))' % a.r_repr())

r('one <- rep(1, 100)')
r('theta <- 0')
r('itembank <- cbind(coeff[,2:1], 1 - one, one)')

replies = student_data[len(student_data) / 2] # random.choice(range(50))
print replies
replied_so_far = []
results_so_far = []
for t in range(50):
	print replied_so_far
	print 'nextItem(itembank, NULL, theta, out = c({}))$item'.format(','.join(map(str, replied_so_far)))
	next_item = r('nextItem(itembank, NULL, theta, out = c({}))$item'.format(','.join(map(str, replied_so_far))))[0]
	print('Tour {} : on pose la question {} au candidat.'.format(t + 1, next_item))
	replied_so_far.append(next_item)
	if replies[next_item - 1]:
		results_so_far.append(1)
		print(u'Il réussit !')
	else:
		results_so_far.append(0)
		print(u'Il échoue !')
	theta = r('theta <- thetaEst(itembank[c({}),], c({}))'.format(','.join(map(str, replied_so_far)), ','.join(map(str, results_so_far))))
	pm = r('semTheta(theta, itembank[c({}),])'.format(','.join(map(str, replied_so_far))))
	print(r.c(theta, pm))
	proba_question = tuple(r('round(Pi(theta, itembank)$Pi, 3)'))
	print 'Résultats / vrais résultats'
	print proba_question
	print map(lambda x: (round(x, 1)), proba_question)
	print ''.join(map(lambda x: str(int(round(x))), proba_question))
	print ''.join(map(lambda x: str(int(x)), replies))
	# next_item = r('nextItem(itembank, NULL, theta, x = c({}), out = c({}))$item'.format(','.join([str(_) for _ in res[:k+1]]), ','.join(replied_so_far)))[0]
	print logloss(proba_question, replies)
