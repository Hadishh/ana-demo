#!/bin/sh

echo 'Waiting for postgres...'
neo4j_uri=$NEO4J_URI

# Remove scheme
HOSTPORT="${neo4j_uri#bolt://}"

# Extract host and port in one line
NEO4J_HOST="${HOSTPORT%%:*}"
NEO4J_PORT="${HOSTPORT##*:}"

while ! nc -z $DB_HOSTNAME $DB_PORT; do
    sleep 0.1
done

while ! nc -z $NEO4J_HOST $NEO4J_PORT; do
    sleep 0.1
done

echo 'PostgreSQL and NEO4j started'

echo 'Running migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input
exec "$@"