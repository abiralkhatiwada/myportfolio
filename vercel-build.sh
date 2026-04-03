#!/bin/bash

# Install dependencies if not already done (Vercel does this automatically usually)
# pip install -r requirements.txt

# Create the staticfiles directory
mkdir -p staticfiles

# Run collectstatic
echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput

echo "Build script completed."
