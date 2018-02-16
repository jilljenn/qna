from my_io import Dataset
from qmatrix import QMatrix
from scipy.sparse import csr_matrix, save_npz
import pandas as pd
import yaml
import random
import os.path


DATASET_NAME = 'fraction'
DATA_FOLDER = '/Users/jilljenn/code/TF-recomm/data'
CSV_FOLDER = os.path.join(DATA_FOLDER, DATASET_NAME)
CSV_TRAIN = os.path.join(CSV_FOLDER, 'train.csv')
CSV_TEST = os.path.join(CSV_FOLDER, 'test.csv')
CSV_VAL = os.path.join(CSV_FOLDER, 'val.csv')
CONFIG = os.path.join(CSV_FOLDER, 'config.yml')
Q_NPZ = os.path.join(CSV_FOLDER, 'qmatrix.npz')


dataset = Dataset(DATASET_NAME)
nb_train = 0
with open(CSV_TRAIN, 'w') as train:
    with open(CSV_TEST, 'w') as test:
        with open(CSV_VAL, 'w') as val:
            for i in range(dataset.nb_students):
                for j in range(dataset.nb_questions):
                    line = ','.join([str(i), str(j), '1' if dataset.data[i][j] else '0', '0', '0']) + '\n'
                    if random.random() < 0.8:
                        nb_train += 1
                        train.write(line)
                    else:
                        test.write(line)
                        val.write(line)


qm = QMatrix()
qm.load('qmatrix-%s' % DATASET_NAME)
save_npz(Q_NPZ, csr_matrix(qm.Q))


with open(CONFIG, 'w') as f:
    config = {
        'USER_NUM': dataset.nb_students,
        'ITEM_NUM': dataset.nb_questions,
        'NB_CLASSES': 2,
        'BATCH_SIZE': nb_train
    }
    f.write(yaml.dump(config, default_flow_style=False))
