#!/bin/bash

rm -rf */migrations/0*.py 
rm -f ./db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata */fixtures/*

# Marketplace downloads tmp folder
mkdir -p /tmp/api/jupyterhub