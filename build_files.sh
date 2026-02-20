#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations (Required for Neon/Production DB)
python manage.py migrate --noinput

# Seed initial data (Only adds if empty)
python manage.py seed_data


