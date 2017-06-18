#!/bin/bash

if [ "$#" -eq 1 ]; then
    python3 JackCompiler.py ${1}
    exit 0
fi

for dir in ../*; do
    python3 JackCompiler.py ${dir}
done

