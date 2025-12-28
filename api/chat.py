from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Physical AI Backend API', 'status': 'running'}).encode())
    
    def do_POST(self):
        if self.path == '/api/v1/chat':
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length).decode())
            msg = body.get('message', '').lower()
            
            if 'hi' in msg or 'hello' in msg:
                resp = "Hello! I'm your Physical AI assistant."
            elif 'walk' in msg:
                resp = "Bipedal walking requires dynamic balance control."
            elif 'control' in msg:
                resp = "PID controllers use P, I, D for error correction."
            elif 'vision' in msg:
                resp = "Computer vision helps robots understand environment."
            elif 'learn' in msg or 'ai' in msg:
                resp = "Machine learning enables robots to improve."
            else:
                resp = "That's an interesting question about robotics!"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'response': resp, 'confidence': 0.85}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
