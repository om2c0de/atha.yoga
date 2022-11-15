#!/bin/sh
gunicorn atha_yoga.wsgi:application --bind 0.0.0.0:8000