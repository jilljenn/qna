import os.path
import sys
import glob

folder = sys.argv[1]

for path in glob.glob('%s/*' % folder):
    if os.path.isdir(path) and not path.endswith('logs'):
        for key in ['mean']:#, 'count', 'delta']:
            print('python plot.py %s %s' % (path, key))
            os.system('python plot.py %s %s' % (path, key))
