#!/bin/bash

# Copyright © Christopher Pratt 2019

if [ "$1" == "help" ] || [ "$1" == "-help" ] || [ "$1" == "--help" ] || [ -z "$1" ]; then
    echo "API packaging script for Elastic Beanstalk. Copyright © Christopher Pratt 2019"
    echo "Usage: ./createZIP.sh environment filename"
    echo "There are currently two options for environment names: production, development"
    exit 0
fi

if [ -z "$2" ]; then
    echo "You must provide a filename."
    exit -1
fi

if [ "$1" -ne "production" ] && [ "$1" -ne "development" ]; then
    echo "You must provide a valid environment: 'production' or 'development' (without quotes)"
    exit -1
fi

if [ "$1" == "production" ]; then
    REMOVE="development"
else
    REMOVE="production"
fi

zip -r $2.zip . -x "venv/*" -x ".git*" -x ".gitignore" -x "__MACOSX*" -x "Clubtalk/storyclip-db.sqlite" -x ".ebextensions/$REMOVE-*.config" -x "createZIP.sh"
