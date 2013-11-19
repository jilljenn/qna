Il faut d'abord installer [virtualenv](https://pypi.python.org/pypi/virtualenv) pour Python 2.7.

Puis gfortran dans [ce humble bundle](http://www.scipy.org/scipylib/building/macosx.html#compilers-c-c-fortran-cython).

    $ virtualenv . && . bin/activate
    $ pip install scipy
    $ pip install numpy
