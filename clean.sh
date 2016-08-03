#!/bin/bash
rm $1/log*
rm $1/stats*
for i in `seq 0 4`
do
    rm $1$i/log*
    rm $1$i/stats*
done
