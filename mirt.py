# coding=utf8
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from calc import logloss, compute_mean_entropy
import random

r = robjects.r
cdm = importr('CDM')
mirt = importr('mirt')
mirtCAT = importr('mirtCAT')

class MIRT():
    q = None
    def __init__(self, q=None, slip=None, guess=None, prior=None, criterion='MFI'):
        self.name = 'MIRT'
        self.criterion = 'MFI'
        self.nb_questions = None
        self.validation_question_set = None
        if q:
            self.q = q
            robjects.globalenv['entries'] = robjects.IntVector(q.get_entries())
        else:
            r('Q <- as.matrix(fraction.subtraction.qmatrix)')
            r('entries <- c()')
            r('for(i in 1:20) { for(j in 1:8) { entries <- c(entries, Q[i, j]) } }')
        r("Q <- matrix(c(entries), ncol=8, dimnames=list(NULL, c('F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8')), byrow=TRUE)")

    def training_step(self, train, opt_Q=True, opt_sg=True):
        nb_students = len(train)
        self.nb_questions = len(train[0])
        raw_data = map(int, reduce(lambda x, y: x + y, train))
        data = r.matrix(robjects.IntVector(raw_data), nrow=nb_students, byrow=True)
        # robjects.globalenv['data'] = data
        r('data <- fraction.subtraction.data')
        r('model = mirt.model(Q)')
        r('fit = mirt(data, model)')
        r('V <- coef(fit, simplify=TRUE)$items[,1:9]')
        # r("U <- cbind(fscores(fit, method='MAP', full.scores=TRUE), rep(1))")
        # r('Z <- U %*% t(V)')

    def load(self, filename):
        pass

    def init_test(self, validation_question_set):
        self.validation_question_set = validation_question_set
        r("CATdesign <- mirtCAT(NULL, fit, criteria='Drule', start_item='Drule', local_pattern=data, design_elements=TRUE)")


    def next_item(self, replied_so_far, results_so_far):
        next_item_id = mirtCAT.findNextItem(r.CATdesign)[0]
        print('Next item', next_item_id - 1)
        return next_item_id - 1

    def estimate_parameters(self, replied_so_far, results_so_far, var_id=''):
        print('estimate', replied_so_far[-1], results_so_far[-1])
        r('CATdesign <- updateDesign(CATdesign, items=c(%s), response=c(%s))' % (replied_so_far[-1] + 1, int(results_so_far[-1])))
        r('CATdesign$person$Update.thetas(CATdesign$design, CATdesign$test)')
        print 'Thêta du candidat :', r('CATdesign$person$thetas')[0]
        # pm = r('semTheta(theta, itembank[c({}),])'.format(','.join(map(str, replied_so_far))))

    def predict_performance(self, var_id=''):
        r('U <- cbind(CATdesign$person$thetas, rep(1))')
        r('Z <- U %*% t(V)')
        r('p <- 1 / (1 + exp(-Z))')
        return tuple(r.p)

    def get_prefix(self):
        prefix = 'mirt'
        if self.q:
            prefix += '-%s' % self.q.get_prefix()
        return prefix
