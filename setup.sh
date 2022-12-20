#!/bin/bash

install() {
    local directory=$1
    echo "Running yarn install in $directory directory."
    cd "$directory" || { echo "Unable to change to $directory project directory"; exit 1; }
    yarn install
    cd - || { echo "Unable to change return to root directory"; exit 1; }
}

clean() {
    local directory=$1
    echo "Removing $directory/node_modules/..."
    cd "$directory" || { echo "Failure to change $directory project directory"; exit 1; }
    rm -rf node_modules/
    cd - || { echo "Failure to change return to root directory"; exit 1; }
}

clean_option="clean"

if [[ $# -ne 0 ]] && [[ $1 -eq $clean_option ]]
then
    clean frontend
fi

install frontend
install system-tests

./etc/etc-hosts.sh local.rosalution.cgds

key=$(head -c 65 < /dev/random | base64 |  tr -dc A-Za-z0-9)
if grep -Fq "ROSALUTION_KEY" ~/.bashrc
then
    replace_value="ROSALUTION_KEY=$key"
    sed "s,ROSALUTION_KEY=[^;]*,$replace_value,"  ~/.bashrc > ~/.bashrc.bak && mv ~/.bashrc.bak ~/.bashrc
    echo "Updating rosalution_key in ~/.bashrc ..."
else
    echo  "export ROSALUTION_KEY=$key" >> ~/.bashrc
    echo "Setting rosalution_key in ~/.bashrc ..."
fi
echo "Source your ~/.bashrc to load the updated environment"
