import http.server
import os
import socketserver

PORT = int(os.environ.get('PORT', '3000'))
WEB_ROOT = os.path.dirname(__file__)

os.chdir(WEB_ROOT)

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

with socketserver.TCPServer(('0.0.0.0', PORT), Handler) as httpd:
    print(f'SmartBin 360 is running at http://localhost:{PORT}')
    httpd.serve_forever()
