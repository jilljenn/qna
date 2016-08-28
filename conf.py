dataset_name = 'timss2003'
PREFIX = dataset_name

STUDENT_FOLD = 4  # 4
QUESTION_FOLD = 2  # 2
BATCH_SIZE = 5

DEBUG = False  # DEBUG == True means only one student
VERBOSE = False

if DEBUG:
    STUDENT_FOLD = 1
    PREFIX = 'tmp'

nb_competences_values = [8] #range(2, 15, 3)

model_names = {
    'mirt': 'MIRT',
    'irt': 'IRT',
    'qm': 'QMatrix',
    'qm-qmatrix-cdm': 'QMatrix',
    'qm-qmatrix-ecpe': 'QMatrix',
    'qm-qmatrix-fake': 'QMatrix',
    'qm-qmatrix-fraction': 'QMatrix',
    'qm-qmatrix-timss2003': 'QMatrix',
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
    'mirt-qm-qmatrix-timss2003': 'MIRT'
}
