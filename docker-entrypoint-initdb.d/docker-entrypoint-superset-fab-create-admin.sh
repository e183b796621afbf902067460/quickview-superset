#!/bin/bash

# create Admin user
superset fab create-admin --username "$SUPERSET_USERNAME" --firstname "$SUPERSET_FIRSTNAME" --lastname "$SUPERSET_LASTNAME" --email "$SUPERSET_EMAIL" --password "$SUPERSET_PASSWORD"

