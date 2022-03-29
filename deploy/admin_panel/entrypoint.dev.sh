#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Wait for PostgreSQL..."

    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL is up!"
fi

echo "Generate translations..."
cd movies/ && python ../manage.py compilemessages --locale ru_RU -v 0 && cd ..

echo "Prepare dev environment..."
python manage.py collectstatic --no-input --clear
python manage.py migrate --fake movies 0001
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py loaddata /home/app/fixtures.json.gz

echo "Starting server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
