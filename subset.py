import json
import random
from conf import dataset_name, nb_competences_values

if dataset_name == 'castor6e':
    question_subset = range(17)
    train_subset = sorted(random.sample(range(58939), 48939))
elif dataset_name == 'fraction':
    question_subset = range(20)
    train_subset = sorted(random.sample(range(536), 436))
elif dataset_name == 'sat':
    question_subset = range(20)
    train_subset = sorted(random.sample(range(296), 216))    

with open('subset.json', 'w') as f:
    f.write(json.dumps({
        'question_subset': question_subset,
        'train_subset': train_subset
    }))
