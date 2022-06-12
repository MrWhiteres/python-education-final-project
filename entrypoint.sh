#!/usr/bin/env bash
pip install -r requirements.txt
export FLASK_APP=project/app
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
gunicorn -b 0.0.0.0:8000 project:app --reload
