#!/bin/bash
echo "--> Starting web process"
gunicorn config.wsgi:application -b 0.0.0.0:80 --log-level debug