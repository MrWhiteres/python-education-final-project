#!/usr/bin/env bash
pip install -r requirements.txt
export FLASK_APP=project/app
export FLASK_ENV=project/
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
gunicorn -w 2 -b 0.0.0.0:8000 wsgi:app --reload