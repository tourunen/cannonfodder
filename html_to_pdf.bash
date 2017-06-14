#!/usr/bin/env bash

for file in $*; do
    echo "converting $file"
    filebase=$(basename $file)
    # htmldoc --no-toc --no-title --no-numbered --footer '   ' --embedfonts --outfile $filebase.pdf $file
    #./node_modules/.bin/html5-to-pdf --page-size A4 --template htmlbootstrap -o $filebase.pdf $file
    ./node_modules/.bin/html5-to-pdf --page-size A4 -o $filebase.pdf $file
done
