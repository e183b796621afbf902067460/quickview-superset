#!/bin/bash

# Upgrading Superset metastore
superset db upgrade

# create Admin user
superset fab create-admin --username "$SUPERSET_USERNAME" --firstname "$SUPERSET_FIRSTNAME" --lastname "$SUPERSET_LASTNAME" --email "$SUPERSET_EMAIL" --password "$SUPERSET_PASSWORD"

# setup roles and permissions
superset init

# run superset server as async process
bash /usr/bin/run-server.sh &

# import charts and dashboards using .py script
python3 /app/docker-entrypoint-initdb.d/docker-entrypoint-initdb.py ;

# kill gunicorn process
pgrep gunicorn | xargs kill ;

# restart superset server as main process
bash /usr/bin/run-server.sh