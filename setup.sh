#!/bin/bash

install() {
    local directory=$1
    echo "Running yarn install in $directory directory."
    cd "$directory" || { echo "Unable to change to $directory project directory"; exit 1; }
    yarn install
    cd ../ || { echo "Unable to change return to root directory"; exit 1; }
}

clean() {
    local directory=$1
    echo "Removing $directory/node_modules/..."
    cd "$directory" || { echo "Failure to change $directory project directory"; exit 1; }
    rm -rf node_modules/
    cd ../ || { echo "Failure to change return to root directory"; exit 1; }
}

clean_option="clean"

if [[ $# -ne 0 ]] && [[ $1 -eq $clean_option ]]
then
    clean frontend
fi

install frontend

./etc/etc-hosts.sh local.divergen.cgds
