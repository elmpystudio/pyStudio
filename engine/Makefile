
.PHONY: run
SHELL=bash

build_docker:
	docker build -t ml_studio --no-cache .
	#docker build -t ml_studio .

run:
	source ./docker_vars.sh && python3.7 pipeline_test.py
