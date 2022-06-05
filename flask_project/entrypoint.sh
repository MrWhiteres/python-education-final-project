#!/usr/bin/env bash
cd app
flask db init
flask db upgrade
cd ..
python3 manage.py runserver
