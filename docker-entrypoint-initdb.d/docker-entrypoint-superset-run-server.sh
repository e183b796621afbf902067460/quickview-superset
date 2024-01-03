#!/bin/bash

# setup superset
bash /usr/bin/run-server.sh &
python3 /app/docker-entrypoint-initdb.d/docker-entrypoint-superset-assets-import.py ;
pgrep gunicorn | xargs kill ;
bash /usr/bin/run-server.sh