import os
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    user_id: str = "anonymous"

class ChatResponse(BaseModel):
    response: str
    confidence: float = 0.8

SAMPLE_RESPONSES = {
    "greeting": [
        "Hello! I'm your Physical AI and Humanoid Robotics assistant. How can I help you today?",
        "Hi there! I'm here to help you learn about robotics and AI. What would you like to know?",
        "Welcome! I can answer questions about humanoid robots, AI, and robotics. What's your question?"
    ],
    "walking": [
        "Bipedal walking is one of the most challenging tasks in robotics. It requires dynamic balance control using concepts like Zero Moment Point (ZMP) for stability.",
        "Humanoid walking involves complex coordination between joints. The robot must maintain balance while moving forward, which requires real-time control systems.",
        "Dynamic walking allows robots to move more naturally by using momentum, unlike static walking where the center of mass stays within the support polygon."
    ],
    "control": [
        "Control systems are the heart of robotics. PID controllers are commonly used: P (Proportional) for current error, I (Integral) for past errors, and D (Derivative) for predicting future errors.",
        "Feedback control is essential in robotics. It allows robots to correct their actions based on sensor feedback and maintain desired behavior.",
        "Modern robots use advanced control techniques like model predictive control and adaptive control to handle complex, dynamic environments."
    ],
    "vision": [
        "Computer vision helps robots understand their environment. Stereo vision provides depth perception, while SLAM (Simultaneous Localization and Mapping) helps robots track their location.",
        "Visual perception in robotics involves object detection, recognition, and scene understanding. Deep learning has revolutionized computer vision capabilities.",
        "Robots use cameras and image processing to navigate, manipulate objects, and interact with humans safely and effectively."
    ],
    "learning": [
        "Machine learning enables robots to improve through experience. Reinforcement learning allows robots to learn from trial and error, while imitation learning lets them copy human demonstrations.",
        "AI in robotics includes neural networks for perception, decision-making algorithms for planning, and adaptive systems that learn from data.",
        "Deep learning has transformed robotics by enabling better perception, more natural movement, and improved human-robot interaction."
    ],
    "design": [
        "Humanoid robot design involves mechanical engineering, electronics, and software integration. Key considerations include degrees of freedom, actuator selection, and weight distribution.",
        "Robot design must balance functionality, safety, and efficiency. Materials like carbon fiber and aluminum are used for lightweight yet strong structures.",
        "Anthropomorphic design helps robots work in human environments and interact naturally with people."
    ],
    "sensors": [
        "Robots use multiple sensors for perception: cameras for vision, IMUs for orientation, force sensors for touch, and LIDAR for distance measurement.",
        "Sensor fusion combines data from multiple sensors to create accurate environmental understanding and robust robot behavior.",
        "Modern robots integrate visual, tactile, and proprioceptive sensing to interact safely and effectively with their environment."
    ],
    "applications": [
        "Humanoid robots are used in healthcare for patient care, manufacturing for assembly tasks, and service industries for customer interaction.",
        "Applications include surgical assistance, elderly care, education, entertainment, and research. Each requires specialized capabilities and safety measures.",
        "Future applications will expand to home assistance, disaster response, space exploration, and collaborative work environments."
    ],
    "default": [
        "That's an interesting question about robotics! Physical AI combines artificial intelligence with embodied systems that interact with the real world.",
        "I can help you understand various aspects of robotics including locomotion, manipulation, perception, control systems, and human-robot interaction.",
        "Robotics is a fascinating field that combines mechanical engineering, computer science, and AI. What specific aspect would you like to explore?",
        "Physical AI involves robots that can perceive, reason, and act in the physical world. This requires integration of sensors, actuators, and intelligent algorithms."
    ]
}

@app.get("/")
def read_root():
    return {"message": "Physical AI Textbook API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/chat")
async def chat_endpoint(chat_message: ChatMessage):
    try:
        message_lower = chat_message.message.lower()
        
        if any(word in message_lower for word in ['hi', 'hello', 'hey', 'assalam', 'salam']):
            response_text = random.choice(SAMPLE_RESPONSES["greeting"])
        elif any(word in message_lower for word in ['walk', 'locomotion', 'gait', 'bipedal', 'balance']):
            response_text = random.choice(SAMPLE_RESPONSES["walking"])
        elif any(word in message_lower for word in ['control', 'pid', 'feedback', 'controller']):
            response_text = random.choice(SAMPLE_RESPONSES["control"])
        elif any(word in message_lower for word in ['vision', 'camera', 'perception', 'see', 'visual', 'slam']):
            response_text = random.choice(SAMPLE_RESPONSES["vision"])
        elif any(word in message_lower for word in ['learn', 'ai', 'machine', 'neural', 'deep', 'algorithm']):
            response_text = random.choice(SAMPLE_RESPONSES["learning"])
        elif any(word in message_lower for word in ['design', 'build', 'construct', 'mechanical', 'structure']):
            response_text = random.choice(SAMPLE_RESPONSES["design"])
        elif any(word in message_lower for word in ['sensor', 'sensing', 'touch', 'feel', 'detect']):
            response_text = random.choice(SAMPLE_RESPONSES["sensors"])
        elif any(word in message_lower for word in ['application', 'use', 'industry', 'healthcare', 'manufacturing']):
            response_text = random.choice(SAMPLE_RESPONSES["applications"])
        else:
            response_text = random.choice(SAMPLE_RESPONSES["default"])
        
        return ChatResponse(response=response_text, confidence=0.85)
    except Exception as e:
        return ChatResponse(
            response="I apologize, but I'm experiencing some technical difficulties. Please try asking your question again.",
            confidence=0.5
        )

@app.get("/api/v1/chapters")
def get_chapters():
    chapters = [
        {"id": 1, "title": "Foundations of Physical AI", "slug": "foundations-of-physical-ai"},
        {"id": 2, "title": "Humanoid Robot Design Principles", "slug": "humanoid-robot-design-principles"},
        {"id": 3, "title": "Locomotion and Bipedal Walking", "slug": "locomotion-and-bipedal-walking"},
        {"id": 4, "title": "Manipulation and Grasping", "slug": "manipulation-and-grasping"},
        {"id": 5, "title": "Perception and Sensing", "slug": "perception-and-sensing"},
        {"id": 6, "title": "Planning and Decision Making", "slug": "planning-and-decision-making"},
        {"id": 7, "title": "Control Systems and Dynamics", "slug": "control-systems-and-dynamics"},
        {"id": 8, "title": "Learning and Adaptation", "slug": "learning-and-adaptation"},
        {"id": 9, "title": "Human-Robot Interaction", "slug": "human-robot-interaction"},
        {"id": 10, "title": "Applications and Use Cases", "slug": "applications-and-use-cases"},
        {"id": 11, "title": "Ethics and Society", "slug": "ethics-and-society"},
        {"id": 12, "title": "Future Directions", "slug": "future-directions-and-conclusions"}
    ]
    return {"chapters": chapters}

handler = Mangum(app, lifespan="off")