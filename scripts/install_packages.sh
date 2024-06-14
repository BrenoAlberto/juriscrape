#!/bin/bash

for dir in /home/juriscrape-dev/juriscrape/*/
do
  if [ -e "$dir/package.json" ]
  then
    echo "Installing dependencies for $dir"
    cd $dir
    npm install
    cd ..
  fi
done