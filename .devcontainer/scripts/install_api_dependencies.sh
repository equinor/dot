#!/bin/bash

sudo apt update
sudo apt -y install graphviz
sudo apt -y install graphviz-dev
sudo apt-get -y install plantuml

python -m pip install --upgrade pip
python -m pip install poetry==1.8.5
poetry --directory ./api install