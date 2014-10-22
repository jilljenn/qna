import json
import math
import matplotlib.pyplot as plt

logloss_qmatrix = json.load(open('data/logloss-qmatrix-all.json'))
logloss_ltm = json.load(open('data/logloss-ltm-all.json'))

nb_students = len(logloss_qmatrix)
budget = len(logloss_qmatrix[0])
print sum([logloss_qmatrix[i][-1] < logloss_ltm[i][-1] for i in range(296)])

fig, ax = plt.subplots()
"""

ax.plot(range(budget), [sorted([logloss_ltm[i][t] for i in range(nb_students)])[nb_students / 4] for t in range(budget)], color='darkblue')
ax.plot(range(budget), [sorted([logloss_ltm[i][t] for i in range(nb_students)])[nb_students / 2] for t in range(budget)], color='blue')
ax.plot(range(budget), [sorted([logloss_ltm[i][t] for i in range(nb_students)])[3*nb_students / 4] for t in range(budget)], color='darkblue')
ax.plot(range(budget), [sorted([logloss_qmatrix[i][t] for i in range(nb_students)])[nb_students / 4] for t in range(budget)], color='darkred')
ax.plot(range(budget), [sorted([logloss_qmatrix[i][t] for i in range(nb_students)])[nb_students / 2] for t in range(budget)], color='red')
ax.plot(range(budget), [sorted([logloss_qmatrix[i][t] for i in range(nb_students)])[3*nb_students / 4] for t in range(budget)], color='darkred')

for lolz in range(nb_students/10):
	ax.plot(range(budget), [sorted([logloss_ltm[i][t] for i in range(nb_students)])[10*lolz] for t in range(budget)], color='blue')
	ax.plot(range(budget), [sorted([logloss_qmatrix[i][t] for i in range(nb_students)])[10*lolz] for t in range(budget)], color='red')
"""
ax.plot(range(budget), [1-math.exp(-sum([logloss_ltm[i][t] for i in range(nb_students)])/nb_students) for t in range(budget)], color='blue')
ax.plot(range(budget), [1-math.exp(-sum([logloss_qmatrix[i][t] for i in range(nb_students)])/nb_students) for t in range(budget)], color='red')
ax.set_title('Median log loss')
plt.show()
