#!/bin/bash

python manage.py migrate
gunicorn config.wsgi -b 0.0.0.0