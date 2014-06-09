# coding=utf8
import rpy2.robjects as robjects
r = robjects.r
r('library(catR)')
r('one <- rep(1, 100)')
r('itembank <- cbind(one, c(1:100)/100, 1 - one, one)')
res = [1, 1, 0, 1, 1, 0, 0, 1]
next_item = 42
replied_so_far = []
for k in range(len(res)):
	print('On pose la question {} au candidat.'.format(next_item))
	replied_so_far.append(str(next_item))
	if res[k]:
		print(u'Il réussit !')
	else:
		print(u'Il échoue !')
	r('theta <- thetaEst(matrix(itembank[c({}),], nrow={}), c({}))'.format(','.join(replied_so_far), k + 1, ','.join([str(_) for _ in res[:k+1]])))
	next_item = r('nextItem(itembank, NULL, theta, x = c({}), out = c({}))$item'.format(','.join([str(_) for _ in res[:k+1]]), ','.join(replied_so_far)))[0]
