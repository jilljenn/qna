#!/bin/bash
# rm -r ectel*
# python subset.py
time python cat.py irt | tee log-irt-$1
# time pypy cat.py qm | tee log-qm-$1
time pypy cat.py qmspe | tee log-qmspe-$1
# time python cat.py mirt | tee log-mirt-$1
time python cat.py mirtq | tee log-mirtq-$1
# time python cat.py baseline | tee log-baseline-$1
# time python cat.py mepv-irt | tee log-mepv-irt-$1
python combine.py
python stats.py
python plot.py ${1}0
