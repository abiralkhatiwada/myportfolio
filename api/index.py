import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from portfolio_site.wsgi import application

class VercelWSGIMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        
        # Check if 'debug-environ' appears in any WSGI environment variable
        show_debug = False
        for k, v in environ.items():
            if isinstance(v, str) and 'debug-environ' in v:
                show_debug = True
                break
                
        if show_debug:
            status = '200 OK'
            response_headers = [('Content-type', 'text/plain; charset=utf-8')]
            start_response(status, response_headers)
            
            lines = [f"{k}: {v}" for k, v in sorted(environ.items()) if isinstance(v, (str, int, float, bool))]
            output = "\n".join(lines).encode('utf-8')
            return [output]
            
        forwarded_uri = environ.get('HTTP_X_FORWARDED_URI', '')
        
        # If the request was rewritten to api/index.py, restore the original path
        if forwarded_uri:
            # Extract only the path part (before the query params '?')
            path = forwarded_uri.split('?')[0]
            environ['PATH_INFO'] = path
        elif 'index.py' in path_info or 'wsgi.py' in path_info:
            environ['PATH_INFO'] = '/'
            
        return self.app(environ, start_response)

app = VercelWSGIMiddleware(application)

