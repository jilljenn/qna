import os, json
import matplotlib.pyplot as plt

"""
loglosses_ltm = json.load(open('data/logloss-ltm.json'))
loglosses_qmatrix = json.load(open('data/logloss-qmatrix.json'))

fig, ax = plt.subplots()
ax.plot(range(len(loglosses_ltm)), loglosses_ltm, color='blue')
ax.plot(range(len(loglosses_qmatrix)), loglosses_qmatrix, color='red')
ax.set_title('Log loss')
plt.show()
"""

#qmatrix = json.load(open('data/' + os.listdir('data')[-1]))['QMatrix']['mean']
irt = json.load(open('data/stats-sat-19062014153953.moyenne-irt-30-80.json'))['IRT']['mean']
qmatrix_bad = json.load(open('data/stats-sat-19062014150413.moyenne-qmatrix.json'))['QMatrix']['mean']
qmatrix = json.load(open('data/stats-sat-19062014153507.moyenne-qmatrix-30-80.json'))['QMatrix']['mean']

fig, ax = plt.subplots()
ax.plot(range(len(irt)), irt, color='blue')
ax.plot(range(len(qmatrix)), qmatrix, color='red')
ax.plot(range(len(qmatrix_bad)), qmatrix_bad, color='green')
ax.set_title('Log loss, improved')
plt.show()
