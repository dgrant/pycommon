#!/bin/sh
pyflakes *.py
pylint --disable=C0301,I0011 --reports=n --errors-only *.py
nosetests --with-coverage --cover-inclusive --cover-html
