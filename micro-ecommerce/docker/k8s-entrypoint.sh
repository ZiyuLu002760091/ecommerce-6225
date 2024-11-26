#!/bin/bash

cd /usr/src/app

if [ ! -f ".env" ]; then
  cp .env.example .env
fi

# Wait for RDS to be ready
echo "Waiting for RDS..."
until python -c "
import sys
import psycopg2
try:
    conn = psycopg2.connect(
        dbname='$POSTGRES_DB',
        user='$POSTGRES_USER',
        password='$POSTGRES_PASSWORD',
        host='$POSTGRES_HOST'
    )
except psycopg2.OperationalError:
    sys.exit(1)
sys.exit(0)
"; do
  echo "RDS is unavailable - sleeping"
  sleep 5
done

echo "RDS is up - executing migrations"

# Run migrations and load data
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fake_data 
python manage.py loaddata initial_data 

# Start the application
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000