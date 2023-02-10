#!/bin/bash

DEBUG=''

if [ "$ROSALUTION_ENV" = "production" ]; then
   DEBUG='-O'
fi

ROSALUTION_KEY="$(< /dev/urandom tr -dc A-Za-z0-9  | head -c 65)" && export ROSALUTION_KEY && \
   python $DEBUG -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level info "$@"