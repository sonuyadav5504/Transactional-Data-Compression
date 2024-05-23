#!/bin/bash
if [ "$1" == "C" ]; then
       python Compression.py "$2" "$3"
fi
if [ "$1" == "D" ]; then
        python Decompression.py "$2" "$3"
fi