#!/usr/bin/env bash
export FLASK_APP=project/app
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
gunicorn -w 4 -b 0.0.0.0:8000 project:app --reload
