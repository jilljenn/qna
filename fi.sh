#!/bin/bash
if [ $1 == "push" ]
then
    tar czf $2.tar.gz $2
    scp $2.tar.gz jj@ulminfo.fr:
elif [ $1 == "pull" ]
then
    scp jj@ulminfo.fr:$2.tar.gz .
    tar xzf $2.tar.gz $1
fi
