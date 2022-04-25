#!/usr/bin/env bash

set -e
set -x

mkdir -p webbpsf-data
FILE_URL='https://www.stsci.edu/~mperrin/software/webbpsf/webbpsf-data-0.9.0.tar.gz'
filename=$(basename $FILE_URL)
filepath="webbpsf-data/$filename"

if [ ! -f "$filepath" ]; then
    echo "Downloading File: $filepath"
    curl $FILE_URL -o $filepath
    cd webbpsf-data
    tar -xf $filename
    cd -
fi
exit 0
