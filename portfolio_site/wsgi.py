import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')

application = get_wsgi_application()

class VercelWSGIMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        forwarded_uri = environ.get('HTTP_X_FORWARDED_URI', '')
        
        # If Vercel rewrote the path (e.g. to wsgi.py or index.py), restore the original path
        if forwarded_uri:
            path = forwarded_uri.split('?')[0]
            environ['PATH_INFO'] = path
        elif 'wsgi.py' in path_info or 'index.py' in path_info:
            environ['PATH_INFO'] = '/'
            
        return self.app(environ, start_response)

app = VercelWSGIMiddleware(application)