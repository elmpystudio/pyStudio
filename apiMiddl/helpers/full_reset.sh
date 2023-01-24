#!/bin/bash

rm -rf */migrations/0*.py 
rm -f ./db.sqlite3
cp ./helpers/settings.py.backup ./rest/settings.py
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata */fixtures/*

# Marketplace downloads tmp folder
rm -r /tmp/api/
mkdir -p /tmp/api/jupyterhub