import json

eden = json.load(open('bundle-eden.json'))
eden2 = json.load(open('bundle-eden2.json'))

for stuff in eden:
	if stuff in ['nbq-20', 'nbq-40']:
		for name in ['irt', '3', '4', '5', '6']:
			for train_power in ['40', '80', '160']:
				eden[stuff][name][train_power] = (eden[stuff][name][train_power] + eden2[stuff][name][train_power]) / 2
	else:
		for i in range(len(eden[stuff])):
			eden[stuff][i] = (eden[stuff][i] + eden2[stuff][i]) / 2

"""
for stuff in ['nbq-20', 'nbq-40']:
	print '%s questions\n' % stuff[-2:]
	print r'\begin{tabular}{cccc}'
	print r'\bfseries ' + ' & '.join(['Train dataset length', '40', '80', '160']) + r'\\'
	print r'\hline'
	for name in ['irt', '3', '4', '5', '6']:
		title = 'IRT' if name == 'irt' else 'Q-matrix %s skills' % name
		line = [title]
		for train_power in ['40', '80', '160']:
			line.append(str(round(eden[stuff][name][train_power], 3)))
		print ' & '.join(line) + r'\\'
	print r'\end{tabular}' + '\n'
"""

"""
print eden['nbq-40']['4']['80']
print eden['nbq-40']['4']['160']

print eden['qmatrix4-80'][19]
print eden['qmatrix4-160'][19]
"""

with open('graph-80.R', 'w') as f:
	f.write('qmatrix3 <- c(%s)\n' % ','.join(map(str, eden['qmatrix3-80'])))
	f.write('qmatrix4 <- c(%s)\n' % ','.join(map(str, eden['qmatrix4-80'])))
	f.write('qmatrix5 <- c(%s)\n' % ','.join(map(str, eden['qmatrix5-80'])))
	f.write('qmatrix6 <- c(%s)\n' % ','.join(map(str, eden['qmatrix6-80'])))
	f.write('irt <- c(%s)\n' % ','.join(map(str, eden['irt-80'])))
	f.write('plot(qmatrix6, type="l", lwd=3)\n')
	# f.write('lines(qmatrix3, type="l")\n')
	f.write('lines(qmatrix4, type="l", lwd=1)\n')
	f.write('lines(qmatrix5, type="l", lwd=2)\n')
	f.write('lines(irt, type="l", xlab="dat", lty="dashed")\n')
	f.write('legend("topright", c("qmatrix3", "qmatrix4", "qmatrix5", "qmatrix6"))\n')

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
