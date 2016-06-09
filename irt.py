# coding=utf8
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from calc import logloss, compute_mean_entropy
from my_io import say
import random

r = robjects.r
ltm = importr('ltm')
cat = importr('catR')

class IRT():
    def __init__(self, Q=None, slip=None, guess=None, prior=None, criterion='MFI'):
        self.name = 'IRT'
        self.criterion = criterion
        self.nb_questions = None
        self.coeff = None
        self.validation_question_set = None

    def training_step(self, train, opt_Q=True, opt_sg=True):
        nb_students = len(train)
        self.nb_questions = len(train[0])
        raw_data = map(int, reduce(lambda x, y: x + y, train))
        a = r.matrix(robjects.IntVector(raw_data), nrow=nb_students, byrow=True)
        model = ltm.rasch(a)
        self.coeff = ltm.coef_rasch(model)
        scores = ltm.factor_scores(model).rx('score.dat')[0].rx('z1')[0]
        r('coeff <- coef(rasch(%s))' % a.r_repr())
        r('one <- rep(1, %d)' % self.nb_questions)
        r('itembank <- cbind(coeff[,2:1], 1 - one, one)')

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
        r('theta{} <- thetaEst(itembank[c({}),], c({}))'.format(var_id, ','.join(map(lambda x: str(x + 1), replied_so_far)), ','.join(map(str, scores_so_far))))

        say('Thêta du candidat :', r('theta')[0])
        # pm = r('semTheta(theta, itembank[c({}),])'.format(','.join(map(str, replied_so_far))))

    def predict_performance(self, var_id=''):
        return tuple(r('round(Pi(theta{}, itembank)$Pi, 3)'.format(var_id)))

    def get_prefix(self):
        return 'irt' if self.criterion == 'MFI' else 'mepv-irt'
