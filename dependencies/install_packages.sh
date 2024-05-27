#!/bin/bash

set -e

sudo apt-get update

sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

if [ -f packages.txt ]; then
    while IFS= read -r package; do
        sudo apt-get install -y "$package"
    done < packages.txt
else
    echo "packages.txt not found."
    exit 1
fi

echo "All packages have been installed."
