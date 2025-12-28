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
            
            # Greetings
            if any(word in msg for word in ['hi', 'hello', 'hey', 'assalam']):
                resp = "Hello! I'm your Physical AI assistant. Ask me about robotics, AI, or humanoid systems!"
            # ROS
            elif 'ros' in msg:
                resp = "ROS 2 is the Robot Operating System - a flexible framework for writing robot software with improved real-time performance and security."
            # Python
            elif 'python' in msg:
                resp = "Python is a popular programming language in robotics for its simplicity and powerful libraries like NumPy, TensorFlow, and ROS bindings."
            # Walking/Locomotion
            elif any(word in msg for word in ['walk', 'locomotion', 'gait', 'bipedal']):
                resp = "Bipedal walking requires dynamic balance control using Zero Moment Point (ZMP) and real-time feedback systems."
            # Control
            elif any(word in msg for word in ['control', 'pid', 'feedback']):
                resp = "PID controllers use Proportional, Integral, and Derivative terms for precise error correction in robotic systems."
            # Vision
            elif any(word in msg for word in ['vision', 'camera', 'perception', 'slam']):
                resp = "Computer vision helps robots understand their environment using cameras, depth sensors, and SLAM algorithms."
            # AI/Learning
            elif any(word in msg for word in ['ai', 'machine learning', 'neural', 'deep learning']):
                resp = "AI enables robots to learn from experience using reinforcement learning, imitation learning, and neural networks."
            # Sensors
            elif any(word in msg for word in ['sensor', 'imu', 'lidar']):
                resp = "Robots use multiple sensors: cameras for vision, IMUs for orientation, LIDAR for distance, and force sensors for touch."
            # Default
            else:
                # Check if question is about robotics
                robotics_keywords = ['robot', 'ai', 'machine', 'sensor', 'control', 'vision', 'learning', 'automation']
                if any(keyword in msg for keyword in robotics_keywords):
                    resp = "I can help with robotics topics like locomotion, control systems, computer vision, AI, sensors, and ROS. What would you like to know?"
                else:
                    resp = "I'm specialized in Physical AI and Robotics. I can answer questions about robot design, control systems, sensors, AI, and humanoid systems. How can I help you with robotics?"
            
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
