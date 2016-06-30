#!/bin/sh
function testcmd {
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        echo "error with $1" >&2
        echo "deploy failed, exiting..."
        exit 1
    fi
    return $status
}

git checkout master
git pull

testcmd ./shell/run_tests.sh

git checkout deploy
git pull
git merge master
git push

git checkout master

echo 'deploy finished successfully!'
