from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from mangum import Mangum

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ChatMessage(BaseModel):
    message: str
    user_id: str = "anonymous"

RESP = {
    "greeting": ["Hello! I'm your Physical AI assistant. How can I help?"],
    "walking": ["Bipedal walking requires dynamic balance control using Zero Moment Point (ZMP)."],
    "control": ["PID controllers use P for current error, I for past errors, D for future errors."],
    "vision": ["Computer vision helps robots understand their environment through stereo vision and SLAM."],
    "learning": ["Machine learning enables robots to improve through experience and reinforcement learning."],
    "design": ["Humanoid robot design involves mechanical engineering, electronics, and software."],
    "sensors": ["Robots use cameras, IMUs, force sensors, and LIDAR for perception."],
    "applications": ["Humanoid robots are used in healthcare, manufacturing, and service industries."],
    "default": ["That's an interesting question about robotics! Physical AI combines AI with embodied systems."]
}

@app.get("/")
def root():
    return {"message": "Physical AI API running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/v1/chat")
async def chat(msg: ChatMessage):
    text = msg.message.lower()
    if any(w in text for w in ['hi', 'hello', 'hey']):
        resp = RESP["greeting"][0]
    elif any(w in text for w in ['walk', 'locomotion', 'gait']):
        resp = RESP["walking"][0]
    elif any(w in text for w in ['control', 'pid']):
        resp = RESP["control"][0]
    elif any(w in text for w in ['vision', 'camera']):
        resp = RESP["vision"][0]
    elif any(w in text for w in ['learn', 'ai']):
        resp = RESP["learning"][0]
    elif any(w in text for w in ['design']):
        resp = RESP["design"][0]
    elif any(w in text for w in ['sensor']):
        resp = RESP["sensors"][0]
    elif any(w in text for w in ['application']):
        resp = RESP["applications"][0]
    else:
        resp = RESP["default"][0]
    return {"response": resp, "confidence": 0.85}

@app.get("/api/v1/chapters")
def chapters():
    return {"chapters": [{"id": i, "title": f"Chapter {i}"} for i in range(1, 13)]}

handler = Mangum(app)