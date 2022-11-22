#!/bin/bash

SRV=developer@35.206.113.210
HOME=/home/developer/ap/frontend
echo "Copying new project in its place"
rsync --delete --recursive --progress `pwd`/dist/* $SRV:$HOME
