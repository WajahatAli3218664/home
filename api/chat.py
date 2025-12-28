from http.server import BaseHTTPRequestHandler
import json
import os
from urllib import request as url_request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Physical AI Backend with LLM', 'status': 'running'}).encode())
    
    def do_POST(self):
        # Accept both '/api/v1/chat' and '/api/v1/chat/' (trailing slash differences)
        if self.path.startswith('/api/v1/chat'):
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length).decode())
            user_msg = body.get('message', '')
            
            # Get API key from Vercel environment variable
            groq_key = os.getenv('GROQ_API_KEY')
            
            if not groq_key:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'response': 'Please configure GROQ_API_KEY in Vercel environment variables.',
                    'confidence': 0.5
                }).encode('utf-8'))
                return
            
            try:
                groq_request = url_request.Request(
                    'https://api.groq.com/openai/v1/chat/completions',
                    data=json.dumps({
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": "You are a helpful Physical AI and Humanoid Robotics expert. Keep responses concise (2-3 sentences)."},
                            {"role": "user", "content": user_msg}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 200
                    }).encode('utf-8'),
                    headers={
                        'Authorization': f'Bearer {groq_key}',
                        'Content-Type': 'application/json'
                    }
                )
                
                with url_request.urlopen(groq_request, timeout=15) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    ai_response = result['choices'][0]['message']['content']

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'response': ai_response, 'confidence': 0.95}).encode('utf-8'))

            except Exception as e:
                # Try to surface HTTP error details when available
                err_msg = str(e)
                try:
                    # If it's an HTTPError from urllib, it may have a code and read() method
                    if hasattr(e, 'code'):
                        err_msg = f'HTTP Error {e.code}: {getattr(e, "reason", "Forbidden")}'
                        try:
                            body = e.read().decode('utf-8')
                            # don't expose sensitive tokens, but include provider message
                            err_msg += f" - {body[:500]}"
                        except Exception:
                            pass
                except Exception:
                    pass

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'response': f'Error: {err_msg}', 'confidence': 0.5}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
