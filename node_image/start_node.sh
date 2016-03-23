#!/bin/bash
#thx http://stackoverflow.com/a/3278427/1092608
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})

if [ $LOCAL = $BASE ]; then
    echo "Need to pull";
    git pull;
    npm install;
fi
echo "Starting server";
npm start;
