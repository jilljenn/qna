import json

eden = json.load(open('bundle-eden.json'))
# eden2 = json.load(open('bundle-eden2.json'))
TRAIN_POWER = '48939'

"""for stuff in eden:
	if stuff in ['nbq-20', 'nbq-40']:
		for name in ['irt', '3', '4', '5', '6']:
			for train_power in ['40', '%s' % TRAIN_POWER, '160']:
				eden[stuff][name][train_power] = (eden[stuff][name][train_power] + eden2[stuff][name][train_power]) / 2
	else:
		for i in range(len(eden[stuff])):
			eden[stuff][i] = (eden[stuff][i] + eden2[stuff][i]) / 2"""

for stuff in ['nbq-17']:
	print '%s questions\n' % stuff[-2:]
	print r'\begin{tabular}{cccc}'
	print r'\bfseries ' + ' & '.join(['Train dataset length', '40', '%s' % TRAIN_POWER, '160']) + r'\\'
	print r'\hline'
	for name in ['irt', '3', '4', '5', '6']:
		title = 'IRT' if name == 'irt' else 'Q-matrix %s skills' % name
		line = [title]
		for train_power in [TRAIN_POWER]:	
			line.append(str(round(eden[stuff][name][train_power], 3)))
		print ' & '.join(line) + r'\\'
	print r'\end{tabular}' + '\n'

"""
print eden['nbq-40']['4']['%s' % TRAIN_POWER]
print eden['nbq-40']['4']['160']

print eden['qmatrix4-%s' % TRAIN_POWER][19]
print eden['qmatrix4-160'][19]
"""

with open('graph-%s.R' % TRAIN_POWER, 'w') as f:
	f.write('qmatrix1 <- c(%s)\n' % ','.join(map(str, eden['qmatrix1-%s' % TRAIN_POWER])))
	f.write('qmatrix3 <- c(%s)\n' % ','.join(map(str, eden['qmatrix3-%s' % TRAIN_POWER])))
	f.write('qmatrix5 <- c(%s)\n' % ','.join(map(str, eden['qmatrix5-%s' % TRAIN_POWER])))
	# f.write('qmatrix6 <- c(%s)\n' % ','.join(map(str, eden['qmatrix6-%s' % TRAIN_POWER])))
	f.write('irt <- c(%s)\n' % ','.join(map(str, eden['irt-%s' % TRAIN_POWER])))
	f.write('plot(qmatrix5, type="l", lwd=5, ann=F)\n')
	# f.write('lines(qmatrix3, type="l")\n')
	f.write('lines(qmatrix1, type="l", lwd=1)\n')
	f.write('lines(qmatrix3, type="l", lwd=3)\n')
	f.write('lines(irt, type="l", xlab="dat", lty="dashed")\n')
	f.write('legend("topright", c("IRT", "Q-matrix K = 1", "Q-matrix K = 3", "Q-matrix K = 5"), lty=c(2, 1, 1, 1), lwd=c(1, 1, 3, 5))\n')
	f.write('title(xlab="Number of questions asked")\n')
	f.write('title(ylab="Mean error")\n')

"""
with open('graph-160.R', 'w') as f:
	f.write('qmatrix3 <- c(%s)\n' % ','.join(map(str, eden['qmatrix3-160'])))
	f.write('qmatrix4 <- c(%s)\n' % ','.join(map(str, eden['qmatrix4-160'])))
	f.write('qmatrix5 <- c(%s)\n' % ','.join(map(str, eden['qmatrix5-160'])))
	f.write('qmatrix6 <- c(%s)\n' % ','.join(map(str, eden['qmatrix6-160'])))
	f.write('irt <- c(%s)\n' % ','.join(map(str, eden['irt-160'])))
	f.write('plot(qmatrix6, type="l", lwd=3)\n')
	# f.write('lines(qmatrix3, type="l")\n')
	f.write('lines(qmatrix4, type="l", lwd=1)\n')
	f.write('lines(qmatrix5, type="l", lwd=2)\n')
	f.write('lines(irt, type="l", xlab="dat", lty="dashed")\n')
	f.write('legend("topright", c("qmatrix3", "qmatrix4", "qmatrix5", "qmatrix6"))\n')
"""