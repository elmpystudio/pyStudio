#!/bin/bash

export AP_MINIO_URL=localhost:9000
export AP_ML_INTERFACE=0.0.0.0
export AP_ML_PORT=5000
export AP_MINIO_ACCESS_KEY=minio
export AP_MINIO_SECRET_KEY=xxxxxxx
export AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=minio
export AWS_SECRET_ACCESS_KEY=xxxxxx
export AP_PG_USER=postgres
export AP_PG_PASS=xxxxxxx
export AP_PG_HOST=localhost
export DAGSTER_HOME=/home/`whoami`/.dagster_home

