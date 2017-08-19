from rpy2.robjects import r
from itertools import product
from math import exp

NB = 20

r('library(catR)')
r('one <- sample(1, %d, T)' % NB)
r('itembank <- cbind(one, c(1:%d)/%d-0.5, 1 - one, one)' % (NB, NB))
print('Here is the item bank: {} questions of increased difficulty'.format(NB))
print(r.itembank)
for pattern in [(0, 1)]: # product((0, 1), repeat=2):
    pattern = pattern + (1, 1)
    print('Student will answer like this:', pattern)
    print()
    questionnaire = [NB // 2]
    for t in range(len(pattern)):
        print('Question %d is asked.' % questionnaire[-1])
        print('Correct!' if pattern[t] else 'Incorrect.')
        questions = ','.join(map(str, questionnaire))
        answers = ','.join(map(str, pattern[:t + 1]))
        r('theta <- thetaEst(matrix(itembank[c(%s),],'
          'nrow=%d), c(%s))' % (questions, t + 1, answers))
        q = r('nextItem(itembank, NULL, theta, x = c(%s),'
              'out = c(%s))$item' % (answers, questions))[0]
        print('Ability estimate:', r.theta[0])
        questionnaire.append(q)
    print('Which means the probability of answering correctly any question is:', [round(1. / (1 + exp(-(r.theta[0] - (float(i + 1) / NB - 0.5)))), 1) for i in range(NB)])
    print()
