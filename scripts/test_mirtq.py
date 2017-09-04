# coding=utf8
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from calc import logloss, compute_mean_entropy
import random

r = robjects.r
cdm = importr('CDM')

r('Q <- as.matrix(fraction.subtraction.qmatrix)')
# print(r("Q"))

r('entries <- c()')
r('for(i in 1:20) { for(j in 1:8) { entries <- c(entries, Q[i, j]) } }')
print(r("entries"))

from qmatrix import QMatrix
q = QMatrix(nb_competences=8)
q.load('qmatrix-cdm')
entries = []
for line in q.Q:
    entries.extend(map(int, line))
print('entries', entries)
robjects.globalenv['entries'] = robjects.IntVector(entries)
print(r("entries"))

r("Q <- matrix(c(entries), ncol=8, dimnames=list(NULL, c('F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8')), byrow=TRUE)")
print(r("Q"))
