#!/bin/bash
# rm -r springer*
. ~/code/bin/activate
python subset.py
time python cat.py irt > log-irt-$1
# time pypy cat.py qm | tee log-qm-$1
time pypy cat.py qmspe | tee log-qmspe-$1
time python cat.py mirt 2 > log-mirt-$1
time python cat.py mirtq > log-mirtq-$1
# time python cat.py mirtqspe | tee log-mirtqspe-$1
# time python cat.py baseline | tee log-baseline-$1
# time python cat.py mepv-irt | tee log-mepv-irt-$1
python combine.py
python stats.py
python plot.py ${1}0
