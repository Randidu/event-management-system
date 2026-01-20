"""
Simple HTTP server to serve frontend files
Run with: python serve_frontend.py
Then open: http://localhost:3000/login.html
"""
import http.server
import socketserver
import os

PORT = 3000
DIRECTORY = "frontend/templates"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("=" * 60)
    print(f"🚀 Frontend server running at http://localhost:{PORT}")
    print("=" * 60)
    print(f"\n📱 Open these URLs in your browser:")
    print(f"   - Login: http://localhost:{PORT}/login.html")
    print(f"   - Home: http://localhost:{PORT}/index.html")
    print(f"   - Events: http://localhost:{PORT}/event_list.html")
    print("\n💡 Press Ctrl+C to stop the server")
    print("=" * 60)
    httpd.serve_forever()
