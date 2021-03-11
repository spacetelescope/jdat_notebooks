#!/usr/bin/env bash

set -e

export LANG=C.UTF-8
export LC_ALL=C.UTF-8

git clone https://github.com/spacetelescope/nbcollection nbcollection
cd nbcollection
git checkout cdb69e5f353c2119d53a85e6a8ae739423ad7df0
pip install -U pip setuptools
pip install -r ci_requirements.txt
python setup.py install
cd -