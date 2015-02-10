import json
import os
from conf import dataset_name

if dataset_name == 'castor6e':
	FOLDER = 'edm-castor'
	FILES = ['2', '5', '8', '11', '14', 'irt']
	TRAIN_POWER = '48939'
elif dataset_name == 'fraction':
	FOLDER = 'edm-fraction'
	FILES = ['2', '5', '8', '11', '14', 'irt', '888']
	TRAIN_POWER = '535'
elif dataset_name == 'sat':
	FOLDER = 'edm-sat'
	FILES = ['2', '5', '8', '11', '14', 'irt']
	TRAIN_POWER = '216'

eden = json.load(open('bundle-%s.json' % FOLDER))
eden2 = json.load(open('bundle-%s2.json' % FOLDER))

for stuff in eden:
	for i in range(len(eden[stuff])):
		eden[stuff][i] = (eden[stuff][i] + eden2[stuff][i]) / 2

"""
for stuff in ['nbq-17']:
	print '%s questions\n' % stuff[-2:]
	print r'\begin{tabular}{cccc}'
	print r'\bfseries ' + ' & '.join(['Train dataset length', '40', '%s' % TRAIN_POWER, '160']) + r'\\'
	print r'\hline'
	for name in FILES:
		title = 'IRT' if name == 'irt' else 'Q-matrix %s skills' % name
		line = [title]
		for train_power in [TRAIN_POWER]:	
			line.append(str(round(eden[stuff][name][train_power], 3)))
		print ' & '.join(line) + r'\\'
	print r'\end{tabular}' + '\n'
"""

"""
print eden['nbq-40']['4']['%s' % TRAIN_POWER]
print eden['nbq-40']['4']['160']

print eden['qmatrix4-%s' % TRAIN_POWER][19]
print eden['qmatrix4-160'][19]
"""

with open('graph-%s.R' % TRAIN_POWER, 'w') as f:
	f.write('qmatrix2 <- c(%s)\n' % ','.join(map(str, eden['qmatrix2-%s' % TRAIN_POWER])))
	f.write('qmatrix5 <- c(%s)\n' % ','.join(map(str, eden['qmatrix5-%s' % TRAIN_POWER])))
	f.write('qmatrix8 <- c(%s)\n' % ','.join(map(str, eden['qmatrix8-%s' % TRAIN_POWER])))
	f.write('qmatrix11 <- c(%s)\n' % ','.join(map(str, eden['qmatrix11-%s' % TRAIN_POWER])))
	f.write('qmatrix14 <- c(%s)\n' % ','.join(map(str, eden['qmatrix14-%s' % TRAIN_POWER])))
	# f.write('qmatrix888 <- c(%s)\n' % ','.join(map(str, eden['qmatrix888-%s' % TRAIN_POWER])))

	f.write('irt <- c(%s)\n' % ','.join(map(str, eden['irt-%s' % TRAIN_POWER])))
	f.write('plot(qmatrix2, type="l", lwd=1, ann=F)\n')
	# f.write('lines(qmatrix5, type="l", lwd=3)\n')
	f.write('lines(qmatrix8, type="l", lwd=3)\n')
	# f.write('lines(qmatrix11, type="l", lwd=7)\n')
	f.write('lines(qmatrix14, type="l", lwd=5)\n')
	f.write('lines(irt, type="l", xlab="dat", lty="dashed")\n')
	f.write('legend("topright", c("IRT", "Q-matrix K = 2", "Q-matrix K = 8", "Q-matrix K = 14"), lty=c(2, 1, 1, 1), lwd=c(1, 1, 3, 5))\n')
	f.write('title(xlab="Number of questions asked")\n')
	f.write('title(ylab="Mean error")\n')
os.system('R --vanilla < graph-%s.R' % TRAIN_POWER)

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