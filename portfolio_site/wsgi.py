"""
WSGI config for portfolio_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')

application = get_wsgi_application()
app = application

# Run migrations and seeding on startup (Vercel cold start)
try:
    print("Starting auto-setup...")
    from django.core.management import call_command
    # Run migrations
    call_command('migrate', no_input=True)
    # Collect static files (Required for Whitenoise)
    call_command('collectstatic', no_input=True)
    # Seed data
    call_command('seed_data', no_input=True)
    print("Auto-setup completed successfully.")
except Exception as e:
    print(f"Startup error in WSGI: {e}")
    import traceback
    traceback.print_exc()
