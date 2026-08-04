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
        
        # Debug endpoint to inspect all headers and environment variables
        if 'debug-environ' in path_info:
            status = '200 OK'
            response_headers = [('Content-type', 'text/plain; charset=utf-8')]
            start_response(status, response_headers)
            
            lines = [f"{k}: {v}" for k, v in sorted(environ.items()) if isinstance(v, (str, int, float, bool))]
            output = "\n".join(lines).encode('utf-8')
            return [output]
            
        forwarded_uri = environ.get('HTTP_X_FORWARDED_URI', '')
        
        print(f"[VercelMiddleware] Original PATH_INFO: {path_info}")
        print(f"[VercelMiddleware] HTTP_X_FORWARDED_URI: {forwarded_uri}")
        
        # If the request was rewritten to api/index.py, restore the original path
        if forwarded_uri:
            # Extract only the path part (before the query params '?')
            path = forwarded_uri.split('?')[0]
            environ['PATH_INFO'] = path
            print(f"[VercelMiddleware] Rewrote PATH_INFO to: {path}")
        elif path_info == '/api/index.py' or path_info == '/api/index.py/':
            environ['PATH_INFO'] = '/'
            print(f"[VercelMiddleware] Defaulted PATH_INFO to: /")
            
        return self.app(environ, start_response)

app = VercelWSGIMiddleware(application)

