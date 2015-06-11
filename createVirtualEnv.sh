#!/bin/sh
rm -rf env2 env3
virtualenv --python python2 env2
env2/bin/pip install --requirement requirements.txt
virtualenv --python python3 env3
env3/bin/pip install --requirement requirements.txt
