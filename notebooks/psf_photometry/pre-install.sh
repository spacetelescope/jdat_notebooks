#!/usr/bin/env bash
set -e

mkdir -p webbpsf-data
FILE_URL='https://stsci.box.com/s/slmgdud1vz9mmbucbsl1bo4dzm9ft4t3'
filename=$(basename $FILE_URL)

if [ ! -f "$filepath" ]; then
    wget https://stsci.box.com/shared/static/34o0keicz2iujyilg4uz617va46ks6u9.gz --no-check-certificate
    tar -xf 34o0keicz2iujyilg4uz617va46ks6u9.gz
    export WEBBPSF_PATH=./webbpsf-data
fi

if [ ! -f "grp" ]; then

    curl -OL http://ssb.stsci.edu/trds/tarfiles/synphot5.tar.gz
    tar -xf synphot5.tar.gz

fi

exit 0
