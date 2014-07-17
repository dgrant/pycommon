#!/bin/sh
set -e

echo "*** Pyflakes"
pyflakes *.py

echo "*** pep8"
pep8 --max-line-length=120  *.py

echo "*** pylint"
pylint --disable=C0301,I0011 --reports=n *.py
