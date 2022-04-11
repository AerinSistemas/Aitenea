#!/bin/bash
python3 manage.py makemigrations accounts
python3 manage.py makemigrations pline
python3 manage.py makemigrations reports
python3 manage.py migrate
python3 manage.py loaddata pline/fixtures/initial_data.json