from calc import logloss, surround
import _io
from qmatrix import QMatrix
import numpypy
import numpy as np

filename = 'sat'

nb_competences = 5
nb_questions = 20
train_power = 160

full_dataset = _io.load(filename, 'data')['student_data'][::-1]
god_prefix = 'qmatrix-%s-%s-%s' % (nb_competences, nb_questions, train_power)
question_subset = range(nb_questions)
dataset = [[full_dataset[i][j] for j in question_subset] for i in range(len(full_dataset))]
train = dataset[:train_power]

model = QMatrix(nb_competences=nb_competences)
# model.load('qmatrix-23092014135654')
model.training_step(train)
"""print 'Error', model.model_error(train)
for i in np.arange(0, 1, 0.1):
    print(i)
    model.slip[0] = i
    print 'Error', model.model_error(train)"""
