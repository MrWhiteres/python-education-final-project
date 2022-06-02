#!/usr/bin/env bash
python3 /flask_project/app/app.py db init
python3 /flask_project/app/app.py db upgrade
python3 /flask_project/manage.py runserver
