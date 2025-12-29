from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Physical AI Backend with Gemini', 'status': 'running'}).encode())
    
    def do_POST(self):
        if self.path.startswith('/api/v1/chat'):
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length).decode())
            user_msg = body.get('message', '')
            
            gemini_key = os.environ.get('GEMINI_API_KEY', 'AIzaSyB-VawC970MxCCPgiJz7FYH-tfCm3AHD5k')
            
            try:
                req_data = json.dumps({
                    "contents": [{
                        "parts": [{"text": f"You are an expert AI assistant for Physical AI and Humanoid Robotics. Provide helpful, accurate responses.\n\nUser: {user_msg}"}]
                    }]
                }).encode('utf-8')
                
                req = urllib.request.Request(
                    f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key}',
                    data=req_data,
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )
                
                with urllib.request.urlopen(req, timeout=15) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    ai_response = result['candidates'][0]['content']['parts'][0]['text']

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'response': ai_response, 'confidence': 0.95}).encode('utf-8'))

            except Exception as e:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'response': f'Error: {str(e)}', 'confidence': 0.5}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
