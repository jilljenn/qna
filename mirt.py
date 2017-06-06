# coding=utf8
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from calc import logloss, compute_mean_entropy, get_train_checksum
from my_io import say, Dataset
from functools import reduce
import dpp
import numpy as np
import random
import os

r = robjects.r
cdm = importr('CDM')
mirt = importr('mirt')
mirtCAT = importr('mirtCAT')

lines = []
def rlog(command):
    global lines
    r(command)
    lines.append(command)


class MIRT:
    q = None
    dim = None
    theta = None
    U = None
    V = None
    dppD = None
    dppV = None
    def __init__(self, dim=2, q=None, slip=None, guess=None, prior=None, criterion='MFI'):
        self.dim = q.nb_competences if q else dim
        self.name = 'MIRT'
        self.criterion = 'MFI'
        self.nb_questions = None
        self.validation_question_set = set()
        if q:
            self.q = q
            robjects.globalenv['entries'] = robjects.IntVector(q.get_entries())
            rlog("Q <- matrix(c(entries), ncol=%d, byrow=TRUE)" % self.dim)  # dimnames=list(NULL, c('F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'))

    def training_step(self, train, opt_Q=True, opt_sg=True):
        prefix = self.get_prefix() if '-' in self.get_prefix() == 'mirtq' else self.get_prefix() + str(self.dim)
        checksum = get_train_checksum(prefix, train)
        self.nb_questions = len(train[0])
        if os.path.isfile('backup/' + checksum + '.rdata'):
            print('Cool, already found!', checksum)
            r.load('backup/' + checksum + '.rdata')
        else:
            nb_students = len(train)
            raw_data = list(map(int, reduce(lambda x, y: x + y, train)))
            data = r.matrix(robjects.IntVector(raw_data), nrow=nb_students, byrow=True)
            data.colnames = robjects.StrVector(['Q%d' % i for i in range(1, self.nb_questions + 1)])
            robjects.globalenv['data'] = data
            if self.q:
                rlog('model = mirt.model(Q)')
                rlog('fit = mirt(data, model, method="MHRM")')#, method="MHRM")')
            elif self.dim < 3:
                rlog('fit = mirt(data, %d)' % self.dim)
            else:
                rlog('fit = mirt(data, %d, method="MHRM")' % self.dim)
            rlog('V <- coef(fit, simplify=TRUE)$items[,1:%d]' % (self.dim + 1))
            print(r.V)
            rlog("U <- cbind(fscores(fit, method='MAP', full.scores=TRUE), rep(1))")
            rlog('save(fit, U, V, data, file="backup/%s.rdata")' % checksum)

        #print(rlog('U[1:5,]'))
        self.U = r('U')
        self.V = r('V')
        rlog('Z <- U %*% t(V)')
        rlog('p <- 1 / (1 + exp(-Z))')
        #print(rlog('Z[1:5,]'))
        #print(rlog('p[1:5,]'))
        #print(rlog('data[1:5,]'))
        """for line in Dataset('banach').data[:5]:
                                                    print(line)"""
        print('Train RMSE:', r('mean((p - data) ** 2) ** 0.5')[0])
        print('Train NLL:', r('-mean(log(abs(p - data)))')[0])
        print('Train accuracy:', r('mean(round(p) == data)')[0])

        similarity = np.array(r.V.dot(r.V.transpose()))
        D, V = np.linalg.eig(similarity)
        self.dppD = np.real(D)
        self.dppV = np.real(V)

    def load(self, filename):
        pass

    def init_test(self, validation_question_set=[]):
        self.validation_question_set = set(validation_question_set)
        rlog("CATdesign <- mirtCAT(NULL, fit, method='ML', criteria='Drule', start_item='Drule', local_pattern=data, design_elements=TRUE)")
        print(rlog('CATdesign'))

    def next_item(self, replied_so_far, results_so_far):
        available_questions = list(map(str, set(range(1, self.nb_questions + 1)) - self.validation_question_set))
        # print('available', available_questions)
        # print(rlog('CATdesign'))
        next_item_id = mirtCAT.findNextItem(r.CATdesign, subset=available_questions)[0]
        print(rlog('CATdesign'))

        say('Next item', next_item_id - 1)

        return next_item_id - 1

    def update_theta(self):
        with open('savesession.txt', 'w') as f:
            f.write('\n'.join(lines))
        rlog('CATdesign$design@Update.thetas(CATdesign$design, CATdesign$person, CATdesign$test)')
        rlog("theta <- cbind(CATdesign$person$thetas, 1)")
        self.theta = r.theta

    def estimate_parameters(self, replied_so_far, results_so_far, var_id=''):
        say('estimate', replied_so_far[-1], results_so_far[-1])

        say('CATdesign <- updateDesign(CATdesign, items=c(%s), response=c(%s))' % (replied_so_far[-1] + 1, int(results_so_far[-1])))
        rlog('CATdesign <- updateDesign(CATdesign, items=c(%s), response=c(%s))' % (replied_so_far[-1] + 1, int(results_so_far[-1])))
        print(rlog('CATdesign$person'))
        self.update_theta()

        say('Thêta du candidat :', rlog('CATdesign$person$thetas'))
        # pm = rlog('semTheta(theta, itembank[c({}),])'.format(','.join(map(str, replied_so_far))))

    def bootstrap(self, chosen, answers):
        items_asked = ','.join(map(lambda x: str(x + 1), chosen))
        answers_got = ','.join(map(lambda x: str(int(x)), answers))
        rlog("CATdesign <- updateDesign(CATdesign, items=c(%s), response=c(%s))" % (items_asked, answers_got))
        self.update_theta()

    def predict_performance(self, var_id=''):
        rlog('U <- cbind(CATdesign$person$thetas, rep(1))')
        rlog('Z <- U %*% t(V)')
        rlog('p <- 1 / (1 + exp(-Z))')
        # print(r.p)
        return tuple(r.p)

    def select_batch(self, batch_size):
        chosen = map(int, dpp.sample_k(batch_size, self.dppD, self.dppV))
        return chosen

    def get_prefix(self):
        prefix = 'mirt'
        if self.q:
            prefix += '-%s' % self.q.get_prefix()
        else:
            prefix += str(self.dim)
        return prefix

    def get_dim(self):
        return self.dim
