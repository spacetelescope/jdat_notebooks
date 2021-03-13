#!/usr/bin/env bash

set -e

if [ ! -z "$CIRCLE_PULL_REQUEST" ]; then
    nbcollection-ci pull-request -u $CIRCLE_PULL_REQUEST
fi