#!/bin/bash

rm -rf */migrations/0*.py 
rm .persistant/db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata */fixtures/*