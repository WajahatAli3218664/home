from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'API running!'}).encode())
        return

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))
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
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
