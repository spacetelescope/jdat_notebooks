#!/bin/bash

apt-get update
apt-get install -y python-virtualenv curl build-essential gcc-4.8
apt-get install -y python-virtualenv
pip install git+https://github.com/eteq/nbpages.git@b9ec8410803357939210e068af7e14a6f0625fab#egg=nbpages
pip install -U pip jupyterlab
