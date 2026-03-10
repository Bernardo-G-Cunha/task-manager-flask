#!/bin/sh

echo "Waiting for database..."

while ! nc -z postgres 5432; do
  sleep 1
done

echo "Database started"

echo "Running migrations..."
flask db upgrade

echo "Starting API..."
gunicorn run:app --bind 0.0.0.0:8000