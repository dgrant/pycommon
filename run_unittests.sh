#!/bin/sh
pyflakes pycommon/*.py
pylint --disable=C0301,I0011 --reports=n --errors-only pycommon/*.py
PYTHONPATH=$PYTHONPATH:.
rm -rf cover .coverage

env2/bin/nosetests --with-coverage --cover-inclusive --cover-html
env3/bin/nosetests --with-coverage --cover-inclusive --cover-html
#nosetests --with-coverage --cover-inclusive --cover-html
