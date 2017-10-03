import rpy2.robjects as robjects
from rpy2.robjects.functions import SignatureTranslatedFunction
from rpy2.robjects.packages import importr
from calc import logloss, compute_mean_entropy
from rpyinterface import RPyInterface
from my_io import say
from functools import reduce
import random
import numpy as np


r = robjects.r
ltm = importr('ltm')
cat = importr('catR')

class IRT(RPyInterface):
    def __init__(self, Q=None, slip=None, guess=None, prior=None, criterion='MFI'):
        self.name = 'IRT'
        self.criterion = criterion
        self.data = None
        self.nb_students = None
        self.nb_questions = None
        self.coeff = None
        self.scores = None
        self.validation_question_set = None

    def compute_all_predictions(self):
        return np.array([self.predict_performance(theta=self.scores[i]) for i in range(self.nb_students)])  # ! Discrimination parameter

    # def compute_all_errors(self, mask):        
    #     print('Train RMSE:', ((((p - self.data) * mask) ** 2).sum() / mask.sum()) ** 0.5)
    #     print('Train NLL:', -np.log(1 - abs(p - self.data) * mask).mean())
    #     print('Train accuracy:', (np.round(p) == self.data).mean())

    def training_step(self, train=None, opt_Q=True, opt_sg=True):
        # self.nb_students = len(train)
        # self.nb_questions = len(train[0])
        # raw_data = list(map(int, reduce(lambda x, y: x + y, train)))
        # self.data = r.matrix(robjects.IntVector(raw_data), nrow=self.nb_students, byrow=True)
        model = ltm.rasch(self.r_data)
        self.coeff = ltm.coef_rasch(model)
        ltm.factor_scores = SignatureTranslatedFunction(ltm.factor_scores, init_prm_translate={'resp_patterns': 'resp.patterns'})  # Mais dans quel monde vivons-nous ma p'tite dame
        self.scores = ltm.factor_scores(model, resp_patterns=self.r_data).rx('score.dat')[0].rx('z1')[0]
        r('data <- %s' % self.r_data.r_repr())
        #r('data[1][1] <- NA')
        r('coeff <- coef(rasch(data))')
        r('one <- rep(1, %d)' % self.nb_questions)
        r('itembank <- cbind(coeff[,2:1], 1 - one, one)')
        # self.compute_all_errors()

    def load(self, filename):
        pass

    def init_test(self, validation_question_set):
        self.validation_question_set = validation_question_set
        r('theta <- 0')

    def next_item(self, replied_so_far, results_so_far):
        if self.criterion == 'MFI':
            available_questions = ['1'] * self.nb_questions
            for question_id in self.validation_question_set:
                available_questions[question_id] = '0'

            say('nextItem(itembank, NULL, theta, nAvailable=c({}), out = c({}), criterion = "{}")$item'.format(','.join(available_questions), ','.join(map(lambda x: str(x + 1), replied_so_far)), self.criterion))
            
            best_question = r('nextItem(itembank, NULL, theta, nAvailable=c({}), out = c({}), criterion = "{}")$item'.format(','.join(available_questions), ','.join(map(lambda x: str(x + 1), replied_so_far)), self.criterion))[0]
            # raise Exception
            return best_question - 1
        # next = random.choice(list(set(range(nb_questions)) - set(replied_so_far)))
        # min_entropy = None
        max_info = None
        best_question = None
        for question_id in range(self.nb_questions):
            if question_id in replied_so_far:
                continue
            p_answering = self.predict_performance()[question_id]
            info = p_answering * (1 - p_answering)
            # self.estimate_parameters(replied_so_far + [question_id], results_so_far + [True], '1')
            # self.estimate_parameters(replied_so_far + [question_id], results_so_far + [False], '0')
            # performance_if_correct = self.predict_performance('1')
            # performance_if_incorrect = self.predict_performance('0')
            # mean_entropy = compute_mean_entropy(p_answering, performance_if_correct, performance_if_incorrect, replied_so_far + [question_id])
            # if not min_entropy or mean_entropy < min_entropy:
            if not max_info or info > max_info:
                # min_entropy = mean_entropy
                max_info = info
                best_question = question_id
        return best_question

    def estimate_parameters(self, replied_so_far, results_so_far, var_id=''):
        scores_so_far = map(int, results_so_far)
        pattern = ['NA'] * self.nb_questions
        for i, pos in enumerate(replied_so_far):
            pattern[pos] = str(int(results_so_far[i]))
        say('theta{} <- thetaEst(itembank, method="ML", c({}))'.format(var_id, ','.join(pattern)))
        r('theta{} <- thetaEst(itembank, method="ML", c({}))'.format(var_id, ','.join(pattern)))

        # r('theta{} <- thetaEst(itembank[c({}),], c({}))'.format(var_id, ','.join(map(lambda x: str(x + 1), replied_so_far)), ','.join(map(str, scores_so_far))))

        say('Thêta du candidat :', r('theta')[0])
        # pm = r('semTheta(theta, itembank[c({}),])'.format(','.join(map(str, replied_so_far))))

    def predict_performance(self, var_id='', theta=None):
        if theta is None:
            return tuple(r('Pi(theta{}, itembank)$Pi'.format(var_id)))
        else:
            return tuple(r('Pi({}, itembank)$Pi'.format(theta)))

    def get_prefix(self):
        return 'irt' if self.criterion == 'MFI' else 'mepv-irt'

    def get_dim(self):
        return 1
