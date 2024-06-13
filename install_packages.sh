#!/bin/bash

for dir in ./*/
do
  if [ -e "$dir/package.json" ]
  then
    echo "Installing dependencies for $dir"
    cd $dir
    npm install
    cd ..
  fi
done