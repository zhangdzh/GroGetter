#!/bin/bash

# run our server locally:
PYTHONPATH=$(pwd):$PYTHONPATH
FLASK_APP=server/endpoints.py flask run --host=127.0.0.1 --port=8000
