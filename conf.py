dataset_name = 'fraction'
PREFIX = 'coldstart'# + dataset_name

#dataset_name = 'banach'
#PREFIX = 'banach-lite'# + dataset_name

STUDENT_TEST_RATE = 0.2
VALIDATION_FOLD = 2
BATCH_SIZE = 10

DEBUG = False  # Debug == TRUE means only one student
VERBOSE = False

nb_competences_values = [8] #range(2, 15, 3)

model_names = {
    'mirt': 'MIRT',
    'irt': 'IRT',
    'qm': 'QMatrix',
    'qm-qmatrix-cdm': 'QMatrix',
    'qm-qmatrix-ecpe': 'QMatrix',
    'qm-qmatrix-fraction': 'QMatrix',
    '8': 'QMatrix',
    '888': 'QMatrix',
    'mepv-irt': 'IRT',
    'baseline': 'Baseline',
    'mirt-qm-qmatrix-cdm': 'MIRT',
    'mirt-qm-qmatrix-cdm-new': 'MIRT',
    'mirt-qm-qmatrix-ecpe': 'MIRT',
    'mirt-qm-qmatrix-banach': 'MIRT',
    'mirt-qm-qmatrix-custom': 'MIRT',
    'mirt-qm-qmatrix-fraction': 'MIRT'
}
