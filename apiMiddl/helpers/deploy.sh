#!/bin/bash

ANALITICS_APP_PROD=""
SRV=developer@ap.entomu.com
HOME=/home/developer/ap/backend

echo "Copying new project in its place `pwd`/"
rsync --exclude "env" --delete --recursive --progress `pwd`/ $SRV:$HOME
#rsync --exclude "env" --delete --recursive --progress `pwd`/.* $SRV:$HOME

# update pip
ssh $SRV "cd $HOME && ./helpers/install_deps.sh"
ssh $SRV "cd $HOME && ANALYTICS_APP_ENV=prod make start_docker"
#ssh $SRV "cd $HOME && make reset_migration"

ssh $SRV "cd $HOME && echo 'Running server' && nohup make run_prod &>log &"
