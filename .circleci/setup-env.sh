#!/usr/bin/env bash

set -e

export LANG=C.UTF-8
export LC_ALL=C.UTF-8

# sudo apt-get update --fix-missing
# sudo apt-get install vim python-virtualenv -y
# sudo apt-get install -y --no-install-recommends \
#         git \
#         make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
#         libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
#         libfreetype6-dev
# 
# sudo apt-get clean

# sudo apt-get install git
pip install -U https://github.com/spacetelescope/nbcollection.git
# git clone https://github.com/spacetelescope/nbcollection nbcollection
# cd nbcollection
# git checkout 5b8f443af1509aa3c0d50115e5efae80d30841ff
# pip install -U pip setuptools
# pip install -r ci_requirements.txt
# python setup.py install
# cd -