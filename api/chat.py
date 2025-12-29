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
        self.wfile.write(json.dumps({'message': 'Physical AI Backend with LLM', 'status': 'running'}).encode())
    
    def do_POST(self):
        if self.path.startswith('/api/v1/chat'):
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length).decode())
            user_msg = body.get('message', '')
            
            groq_key = os.environ.get('GROQ_API_KEY', '')
            
            if not groq_key:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'response': 'API key not configured',
                    'confidence': 0.5
                }).encode('utf-8'))
                return
            
            try:
                req_data = json.dumps({
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": "You are an expert AI assistant for Physical AI and Humanoid Robotics. Provide helpful, accurate responses."},
                        {"role": "user", "content": user_msg}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                }).encode('utf-8')
                
                req = urllib.request.Request(
                    'https://api.groq.com/openai/v1/chat/completions',
                    data=req_data,
                    headers={
                        'Authorization': f'Bearer {groq_key}',
                        'Content-Type': 'application/json'
                    },
                    method='POST'
                )
                
                with urllib.request.urlopen(req, timeout=15) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    ai_response = result['choices'][0]['message']['content']

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'response': ai_response, 'confidence': 0.95}).encode('utf-8'))

            except urllib.error.HTTPError as e:
                err_msg = f'HTTP {e.code}: {e.reason}'
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'response': f'Error: {err_msg}', 'confidence': 0.5}).encode('utf-8'))
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
