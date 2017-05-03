#!/usr/bin/env bash

for file in $*; do
    echo "converting $file"
    filebase=$(basename $file)
    htmldoc --no-toc --no-title --no-numbered --outfile $filebase.pdf $file
done
