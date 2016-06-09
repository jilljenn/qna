dataset_name = 'fraction'
PREFIX = 'ectelbis'# + dataset_name

STUDENT_TEST_RATE = 0.2
DEBUG = False
VERBOSE = False

nb_competences_values = [8] #range(2, 15, 3)

model_names = {
    'mirt': 'MIRT',
    'irt': 'IRT',
    'qm': 'QMatrix',
    'qm-qmatrix-cdm': 'QMatrix',
    '8': 'QMatrix',
    '888': 'QMatrix',
    'mepv-irt': 'IRT',
    'baseline': 'Baseline',
    'mirt-qm-qmatrix-cdm': 'MIRT',
    'mirt-qm-qmatrix-custom': 'MIRT'
}
