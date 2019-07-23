#!/usr/bin/env bash
rm -rf dist/
env3/bin/python3 setup.py sdist bdist_wheel
env3/bin/twine upload --repository-url https://test.pypi.org/legacy/ dist/*
