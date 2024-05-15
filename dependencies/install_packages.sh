#!/bin/bash

set -e

# Update the package list
sudo apt-get update

# Install prerequisites for adding new repositories
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Download and install Filebeat
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.16.3-amd64.deb
sudo dpkg -i filebeat-7.16.3-amd64.deb

# Install packages listed in packages.txt
sudo xargs -a packages.txt apt-get install -y

echo "All packages have been installed."
