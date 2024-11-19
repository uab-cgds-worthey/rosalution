#!/bin/bash

python3 -m venv screen_capture_annotate_env

# shellcheck source=/dev/null
source screen_capture_annotate_env/bin/activate

# install requirements
pip3 install -r requirements.txt

# deactivate venv and return to root directory
deactivate

mkdir -p tmp