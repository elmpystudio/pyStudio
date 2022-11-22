#!/bin/bash

# delete old env to be sure new pckges got installed
rm -rf env

# kill old servers
ps aux | grep python | grep manage | grep runserver | grep develop | cut -d " " -f 2 | xargs kill -9

# new venv
python3 -m venv env
source env/bin/activate
echo "[+] Upgrading pip"
pip3 install --upgrade pip

# delete pkg package coz ubuntu bug
grep -v pkg requirements.txt > new_req
mv new_req requirements.txt

# install new deps

python3 -m pip install wheel
python3 -m pip install -r requirements.txt
