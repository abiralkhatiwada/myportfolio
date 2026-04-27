#!/bin/bash

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create the staticfiles directory
mkdir -p staticfiles

# Run collectstatic
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Run migrations
echo "Running migrations..."
python3 manage.py migrate --noinput

echo "Build script completed."

