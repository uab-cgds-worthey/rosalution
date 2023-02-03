#!/bin/bash
# shellcheck source=/dev/null

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
    rm -rf backend/rosalution_env
fi

install frontend
install system-tests

./etc/etc-hosts.sh local.rosalution.cgds

# change to backend directory, create venv, and activate it
cd backend || { echo "Failure to change to backend directory"; exit 1;}
python3 -m venv rosalution_env
source rosalution_env/bin/activate

# install requirements
pip3 install -r requirements.txt

# deactivate venv and return to root directory
deactivate
cd - || { echo "Unable to change return to root directory"; exit 1; }
echo "Use 'source backend/rosalution_env/bin/activate' to activate the virtual environment"
