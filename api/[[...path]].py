import json

def handler(request):
    if request.method == 'POST' and '/chat' in request.path:
        body = json.loads(request.body)
        msg = body.get('message', '').lower()
        
        if any(w in msg for w in ['hi', 'hello']):
            resp = "Hello! I'm your Physical AI assistant."
        elif any(w in msg for w in ['walk', 'locomotion']):
            resp = "Bipedal walking requires dynamic balance control using ZMP."
        elif any(w in msg for w in ['control', 'pid']):
            resp = "PID controllers use P, I, D for error correction."
        elif any(w in msg for w in ['vision', 'camera']):
            resp = "Computer vision helps robots understand their environment."
        elif any(w in msg for w in ['learn', 'ai']):
            resp = "Machine learning enables robots to improve through experience."
        else:
            resp = "That's an interesting question about robotics!"
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'response': resp, 'confidence': 0.85})
        }
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'message': 'Physical AI API running!'})
    }