import my_io
import sys

for line in my_io.load(sys.argv[1], prefix='data')['student_data']:
    print(line)
