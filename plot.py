import json
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

# qmatrix = json.load(open('data/stats-sat-16062014031727.json'))['QMatrix']['mean']
ltm = json.load(open('data/stats-sat-19062014124758.json'))['IRT']['mean']

fig, ax = plt.subplots()
ax.plot(range(len(ltm)), ltm, color='blue')
# ax.plot(range(len(qmatrix)), qmatrix, color='red')
ax.set_title('Log loss, improved')
plt.show()
