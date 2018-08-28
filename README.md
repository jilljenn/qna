# Comparing models for adaptive testing

Code comparing the Rasch (IRT), DINA, MIRT, GenMA models, presented in our article **Adaptive Testing Using a General Diagnostic Model** featured at the EC-TEL 2016 conference.

    @inproceedings{Vie2016ECTEL,
        Author = {Vie, Jill-J{\^e}nn and Popineau, Fabrice and Bourda, Yolaine and Bruillard, {\'E}ric},
        Booktitle = {European Conference on Technology Enhanced Learning},
        Hyphenation = {english},
        Organization = {Springer},
        Pages = {331--339},
        Title = {Adaptive Testing Using a General Diagnostic Model},
        Year = {2016}}

Comments are welcome! See Authors below.  
You might also be interested in my [tutorial for Knowledge Tracing Machines](https://github.com/jilljenn/ktm) presented at the [Optimizing Human Learning workshop](https://humanlearn.io) in June 2018.

## Requirements

- Python 3 (2.7 works as well if you replace `raw_input` with `input` in `stats.py`)
- Successfully tested on Python 3.6.5 (2018-08-28) and R 3.3.3 (2017-03-06) 3.5.1 (2018-08-28).

``pypy`` is optional but I strongly suggest it for the DINA model, which is pretty slow to train.

As scikit-learn relies on scipy, you may need [gfortran](http://www.scipy.org/scipylib/building/macosx.html#compilers-c-c-fortran-cython) as well.

    $ mkdir backup
    $ python3 -m venv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

This code also relies on R packages, that you will have to install:

- ltm ≥ 1.0.0
- catR ≥ 3.12
- CDM ≥ 5.5-21
- mirt ≥ 1.24
- mirtCAT ≥ 1.5

Or simply type `Rscript install.R` (this takes such a long time!).

## Troubleshooting

You may need to do the following while installing RPy: ``apt-get install libreadline-dev liblzma-dev python-tk``.  
Or `brew install libomp` on Mac OS X.

## Usage

### Strong generalization

Here we separate the existing users into two categories: some for train, and some for adaptive testing. We keep a validation set of questions.

    ./start.sh tmp

You can check options in the `conf.py` file. By default, it should be in ``DEBUG`` mode, which means it focuses on making an adaptive test on only one student. You can change it by setting the ``DEBUG`` parameter to ``False``.

- Rasch: 4s
- DINA 8-dim: 2min or 8s using pypy
- GenMA 8-dim: 3min

### Weak generalization

Perform cross validation on Fraction dataset with all models described in `cv.py` (constant baseline, IRT, DINA, MIRT *d = 2*, MIRT *d = 3*, GenMA):

    python cv.py  # Outputs a lot, should take ~6 min in total

## License

The code is under license **AGPLv3**.

## Authors

- Jill-Jênn Vie <vie@jill-jenn.net>
- Jean-Bastien Grill
