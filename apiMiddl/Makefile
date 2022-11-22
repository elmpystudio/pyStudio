
PY=python3
SHELL := /bin/bash

# with source
WS=source env/bin/activate &&

# Test command, to test scripts with django shell
# TODO
test:
	${WS} ${PY} helpers/tab_utils.py test

run_nginx_local:
1. 	docker-compose -f .persistant/nginx/docker-compose.yaml up -d

start_docker_local:
	export ANALYTICS_APP_ENV=local && docker-compose build && docker-compose up --build -d

start_docker_prod:
	export ANALYTICS_APP_ENV=prod && docker-compose build && docker-compose up --build -d

shell:
	${WS} ${PY} manage.py shell

smoke: 
4.	${WS} $(PY) tests/smoke/run.py no-registry

reset_migration:
	export ANALYTICS_APP_ENV=local && ${WS} ./helpers/reset_migrations.sh

deploy:
	./helpers/deploy.sh

run_prod: 
	 ${WS} ANALYTICS_APP_ENV=prod ${PY} manage.py runserver 0.0.0.0:8000

run: 
3.	 ${WS} ANALYTICS_APP_ENV=local ${PY} manage.py runserver 127.0.0.1:8000
	
start_venv:
	${PY} -m venv env

install_deps:
	${WS} ${PY} -m pip install --upgrade pip
	${WS}	${PY} -m pip install -r requirements.txt

2. install: start_venv install_deps reset_migration

###################
# Tableau utils
###################
tab_list_datasources:
	${WS} ${PY} helpers/tab_utils.py tab_list_datasources

tab_list_projects:
	#${WS} ${PY} helpers/tab_utils.py tab_list_projects
	make shell < helpers/tab_list_projects.py

tab_reset_users:
	make shell < helpers/tab_reset_users.py

tab_list_users:
	${WS} ${PY} helpers/tab_utils.py tab_list_users

tab_list_workbooks:
	${WS} ${PY} helpers/tab_utils.py tab_list_workbooks

tab_test:
	${WS} ${PY} helpers/tab_utils.py test 
