dataset_name = 'fraction'
PREFIX = '2017/fraction'

STUDENT_FOLD = 4
QUESTION_FOLD = 2

DEBUG = False  # DEBUG == True means only one student
VERBOSE = False

if DEBUG:
    STUDENT_FOLD = 1
    PREFIX = 'tmp'

nb_competences_values = [3] #range(2, 15, 3)

model_names = {
    'mirt': 'MIRT',
    'irt': 'IRT',
    'qm': 'QMatrix',
    'qm-qmatrix-cdm': 'QMatrix',
    'qm-qmatrix-ecpe': 'QMatrix',
    'qm-qmatrix-ecpe2': 'QMatrix',
    'qm-qmatrix-fake': 'QMatrix',
    'qm-qmatrix-fraction': 'QMatrix',
    'qm-qmatrix-fraction2': 'QMatrix',
    'qm-qmatrix-timss2003': 'QMatrix',
    'qm-qmatrix-timss2003b': 'QMatrix',
    'qm-qmatrix-castor6e': 'QMatrix',
    'qm-qmatrix-castor6e2': 'QMatrix',
    'qm-qmatrix-sat': 'QMatrix',
    'qm-qmatrix-sat2': 'QMatrix',
    'qm-qmatrix-sat3': 'QMatrix',
    'qm-qmatrix-sat4': 'QMatrix',
    '8': 'QMatrix',
    '888': 'QMatrix',
    'mepv-irt': 'IRT',
    'baseline': 'Baseline',
    'mirt-qm-qmatrix-cdm': 'MIRT',
    'mirt-qm-qmatrix-cdm-new': 'MIRT',
    'mirt-qm-qmatrix-ecpe': 'MIRT',
    'mirt-qm-qmatrix-banach': 'MIRT',
    'mirt-qm-qmatrix-custom': 'MIRT',
    'mirt-qm-qmatrix-fake': 'MIRT',
    'mirt-qm-qmatrix-fraction': 'MIRT',
    'mirt-qm-qmatrix-timss2003': 'MIRT',
    'mirt-qm-qmatrix-sat': 'MIRT',
    'cat': 'cat',
    'dpp': 'dpp',
    'random': 'random',
    'uncertainty': 'uncertainty'
}

strategies = ['random', 'dpp', 'uncertainty']
