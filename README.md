# Comparing models for adaptive testing

Comparing Rasch, DINA, MIRT, GenMA presented at the EC-TEL 2016 conference.

You first need to install [virtualenv](https://pypi.python.org/pypi/virtualenv) for Python 2.7. ``pypy`` is optional but I strongly suggest it for the DINA model, which is pretty slow to train.

As scikit-learn relies on scipy, you may need [gfortran](http://www.scipy.org/scipylib/building/macosx.html#compilers-c-c-fortran-cython) as well.

    $ mkdir backup
    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

This code also relies on R packages, that you will have to install:

- ltm
- catR
- CDM
- mirt
- mirtCAT

## Troubleshooting

You may need to do the following while installing RPy: ``apt-get install libreadline-dev liblzma-dev python-tk``.

## Usage

Either you try a ``./start.sh tmp``, or you check the ``start.sh`` file.

The default ``conf.py`` file is in ``DEBUG`` mode, which means it focuses on making an adaptive test on only one student. You can change it by setting the ``DEBUG`` parameter to ``False``.

- Rasch: 3s
- DINA 8-dim: 40s or 8s using pypy
- MIRT 2-dim: 20s
- GenMA 8-dim: 95s

# License

The code is under license **AGPLv3** which roughly means, you can use it for commercial purposes, even plugging it to proprietary source code, but if you modify it for your needs, you need to publish your changes.

# Author

Jill-Jênn Vie <vie@jill-jenn.net>
