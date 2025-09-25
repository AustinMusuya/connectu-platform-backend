#!/usr/bin/env bash


# Exit on error
set -o errexit

# Install dependencies gracefully
pip install -r requirements.txt

pip install django-graphql-auth

pip install git+https://github.com/flavors/django-graphql-jwt.git@main

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py makemigrations
python manage.py migrate

