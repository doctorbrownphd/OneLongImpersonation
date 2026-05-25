"""
One Long Impersonation -- Local Development Server
Serves the static site on localhost:8080.

Usage: python serve.py
Then open http://localhost:8080/site/
"""

import http.server
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # CORS for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == "__main__":
    with http.server.HTTPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}/site/")
        print(f"Chapters at http://localhost:{PORT}/chapters/01-teachers/")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()
