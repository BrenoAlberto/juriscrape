#!/bin/bash

dirs=$(find /home/juriscrape-dev/juriscrape/ -maxdepth 2 -name 'package.json' -exec dirname {} \;)

echo "$dirs" | xargs -I {} -P 4 bash -c 'cd "{}" && echo "Installing dependencies for {}" && npm install'