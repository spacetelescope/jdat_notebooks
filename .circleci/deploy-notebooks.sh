#!/usr/bin/env bash

set -e
set -x
# Only runs on master
if [ -z "${CIRCLE_PULL_REQUEST}" ]; then
    git config --global user.email devnull@circleci.com
    git config --global user.name CircleCI
    mkdir -p ~/.ssh
    echo 'Host * ' >> ~/.ssh/config
    echo '  StrictHostKeyChecking no' >> ~/.ssh/config
    # Deploy gh-pages
    git clone -b gh-pages --single-branch ${CIRCLE_REPOSITORY_URL} /tmp/out
    cd /tmp/out
    rm -rf pages
    mv /tmp/artifacts-html pages
    rm index.html || true
    mv pages/index.html .
    git add index.html -f
    git add pages -f
    rm -rf .circleci
    git commit -m 'Automated deployment to Github Pages: ${BUILD_TAG}' -a || true
    git push origin gh-pages
    git clean -dfx
fi
exit 0
