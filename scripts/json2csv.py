import sys
import json

filename = sys.argv[1]
with open('data/%s.json' % filename) as f:
    j = json.load(f)
    with open('data/%s.csv' % filename, 'w') as g:
        nb_questions = len(j['Q'][0])
        g.write(','.join(map(lambda x: 'Item %d' % x, range(1, nb_questions + 1))) + '\n')  # Items
        for line in j['Q']:
            g.write(','.join(map(lambda x: str(int(x)), line)) + '\n')
