#!/usr/bin/env bash
#source .venv/bin/activate
gunicorn -w 2 -b 0.0.0.0:5000 wsgi:app
