#!/usr/bin/env bash

if [ ! -d env ]; then
    virtualenv -p python2.7 --clear env
fi
if [ ! -d build ]; then
    mkdir build/
fi

echo ">>> Activate python virtualenv: source env/bin/activate"
