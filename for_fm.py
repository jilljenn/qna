from my_io import Dataset
import yaml
import random
import os


dataset = Dataset('berkeley')
nb_train = 0
with open('/tmp/train.csv', 'w') as train:
    with open('/tmp/test.csv', 'w') as test:
        for i in range(dataset.nb_students):
            for j in range(dataset.nb_questions):
                line = ','.join([str(i), str(j), '1' if dataset.data[i][j] else '0', '0', '0']) + '\n'
                if random.random() < 0.8:
                    nb_train += 1
                    train.write(line)
                else:
                    test.write(line)

os.system('cp /tmp/test.csv /tmp/val.csv')

with open('/tmp/config.yml', 'w') as f:
    config = {
        'USER_NUM': dataset.nb_students,
        'ITEM_NUM': dataset.nb_questions,
        'NB_CLASSES': 2,
        'BATCH_SIZE': nb_train
    }
    f.write(yaml.dump(config, default_flow_style=False))
