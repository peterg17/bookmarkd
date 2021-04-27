#!/bin/sh
export FLASK_APP=bookmarkd:app
# export DD_PROFILING_ENABLED=true
# export DD_SERVICE=app
flask run --host=0.0.0.0 --port=5050
# ddtrace-run python app.py
# python app.py
