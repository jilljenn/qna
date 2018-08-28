#!/bin/bash
python subset.py
mkdir -p $1/logs
time python cat.py irt > $1/logs/irt
time python cat.py qmspe > $1/logs/qmspe  # If you have pypy, it's faster
# time python cat.py qmspe > $1/logs/qmspe
# time python cat.py mirt 2 > $1/logs/mirt  # Now exploratory models such as MIRT can't be used for CAT
time python cat.py mirtq > $1/logs/mirtq
# time python cat.py genma 8 > $1/logs/genma
# time python cat.py mirtqspe | tee log-mirtqspe-$1
# time python cat.py baseline | tee log-baseline-$1
# time python cat.py mepv-irt | tee log-mepv-irt-$1
python combine.py
python stats.py
python plot.py ${1} mean
python plot.py ${1} count
