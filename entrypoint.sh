#!/bin/bash

# Warten, bis die Datenbank erreichbar ist
echo 'Waiting for the database to become available...'
./wait-for-it.sh db:5432 -t 60 -- echo 'Database is available now...'

# Datenbankmigration
echo 'Starting database migration...'
flask db migrate
flask db upgrade

# Starte die App
echo 'Starting the app...'
gunicorn -w 4 -b 0.0.0.0:8000 'bookingapp:create_app()'
