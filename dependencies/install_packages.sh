#!/bin/bash

set -e

# Update the package list
sudo apt-get update

# Install prerequisites for adding new repositories
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Elastic APT repository for filebeat
curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo sh -c 'echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" > /etc/apt/sources.list.d/elastic-7.x.list'

# Update package list again to include the new repository
sudo apt-get update

# Read the packages.txt file and install each package
while IFS= read -r package; do
    sudo apt-get install -y "$package"
done < packages.txt

echo "All packages have been installed."
