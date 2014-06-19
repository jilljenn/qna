# coding=utf8
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

qmatrix = json.load(open('data/' + os.listdir('data')[-1]))['QMatrix']['mean']
irt = json.load(open('data/' + os.listdir('data')[-1]))['IRT']['mean']
#irt = json.load(open('data/stats-sat-19062014153953.moyenne-irt-30-80.json'))['IRT']['mean']
#qmatrix_bad = json.load(open('data/stats-sat-19062014150413.moyenne-qmatrix.json'))['QMatrix']['mean']
#qmatrix = json.load(open('data/stats-sat-19062014153507.moyenne-qmatrix-30-80.json'))['QMatrix']['mean']

# Fake data
# qmatrix = json.load(open('data/stats-fake_data-19062014163005.json'))['QMatrix']['mean']
# irt = json.load(open('data/stats-fake_data-19062014163005.json'))['IRT']['mean']

# Old data
# qmatrix_old = json.load(open('data/stats-sat-19062014164114.OMG.json'))['QMatrix']['mean']
# irt_old = json.load(open('data/stats-sat-19062014164114.OMG.json'))['IRT']['mean']

# Old data 2
# qmatrix = json.load(open('data/stats-sat-19062014164957.json'))['QMatrix']['mean']
# irt = json.load(open('data/stats-sat-19062014164957.json'))['IRT']['mean']

# Big data K = 5
# qmatrix = json.load(open('data/stats-sat-19062014190158.arf.5-comp.json'))['QMatrix']['mean']
# irt = json.load(open('data/stats-sat-19062014190158.arf.5-comp.json'))['IRT']['mean']

# Big data K = 4
# data = json.load(open('data/stats-sat-19062014191840.json'))

# Big data K = 4 α = 0.01
# data = json.load(open('data/stats-sat-19062014192051.json'))

# Big data K = 5 α = 0.01
# data = json.load(open('data/stats-sat-19062014192621.json'))

# Big data K = 5 α = 0.001
data = json.load(open('data/stats-sat-19062014195517.json'))
qmatrix = data['QMatrix']['mean']

# Big data K = 5 α = 0.000
data = json.load(open('data/stats-sat-19062014200009.json'))

qmatrix_zero = data['QMatrix']['mean']
irt = json.load(open('data/stats-sat-19062014192621.json'))['IRT']['mean']
qmatrix_old = json.load(open('data/stats-sat-19062014192621.json'))['QMatrix']['mean']

fig, ax = plt.subplots()
ax.plot(range(len(irt)), irt, color='blue')
ax.plot(range(len(qmatrix)), qmatrix, color='red')
ax.plot(range(len(qmatrix)), qmatrix_old, color='purple')
ax.plot(range(len(qmatrix)), qmatrix_zero, color='orange')
ax.set_title('Log loss, improved')
plt.show()
