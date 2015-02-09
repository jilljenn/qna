import json
import random

with open('subset.json', 'w') as f:
    f.write(json.dumps({
        'question_subset': range(20), # sorted(random.sample(range(40), 40)),
        'train_subset': sorted(random.sample(range(536), 436)) # sorted(random.sample(range(296), 216))
    }))
