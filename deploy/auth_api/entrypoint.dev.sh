#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Wait for PostgreSQL..."

    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL is up!"
fi

echo "Prepare dev environment..."
flask db upgrade
flask createsuperuser -u admin -e example@email.com -p password
flask loaddata

echo "Starting server..."
exec flask run -h 0.0.0.0
