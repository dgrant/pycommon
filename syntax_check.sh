#!/bin/sh
set -e

echo "*** flake8"
flake8 --max-complexity=10 --max-line-length=120 *.py

echo "*** pylint"
pylint --disable=C0301,I0011 --reports=n *.py
