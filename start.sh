#!/bin/bash
# python subset.py
time python cat.py irt | tee log-irt-$1
time pypy cat.py qm | tee log-qm-$1
# time pypy cat.py qmspe | tee log-qmspe-$1
time python cat.py baseline | tee log-baseline-$1
# time python cat.py mepv-irt | tee log-mepv-irt-$1
python plot.py $1
