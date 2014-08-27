#!/bin/sh
pyflakes pycommon/*.py
pylint --disable=C0301,I0011 --reports=n --errors-only pycommon/*.py
PYTHONPATH=$PYTHONPATH:.
rm -rf cover .coverage
nosetests --with-coverage --cover-inclusive --cover-html
