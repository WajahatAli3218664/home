import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import random
from groq import Groq

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Physical AI Textbook API",
    description="API for Physical AI & Humanoid Robotics Textbook with RAG Chatbot",
    version="1.0.0"
)

# Initialize Groq client
groq_client = None
groq_api_key = os.getenv("GROQ_API_KEY")
print(f"GROQ_API_KEY found: {'Yes' if groq_api_key else 'No'}")
if groq_api_key:
    try:
        groq_client = Groq(api_key=groq_api_key)
        print("Groq client initialized successfully")
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
else:
    print("No GROQ_API_KEY found in environment")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
        "https://*.github.io",
        "https://effective-cod-5g46g9pww5pxc7g96-3000.app.github.dev",
        "https://effective-cod-5g46g9pww5pxc7g96-8000.app.github.dev",
        "https://home-pi-one.vercel.app",
        "https://home-cycxez9ru-wajahat-alis-projects-0e7870c5.vercel.app"
    ],
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

# Book content context for the LLM
BOOK_CONTEXT = """
You are an expert AI assistant for a Physical AI and Humanoid Robotics textbook. You have deep knowledge about:

1. Foundations of Physical AI - embodied intelligence, sensor-motor integration
2. Humanoid Robot Design - mechanical design, actuators, degrees of freedom
3. Locomotion and Bipedal Walking - ZMP, dynamic balance, gait patterns
4. Manipulation and Grasping - end-effectors, force control, dexterous manipulation
5. Perception and Sensing - computer vision, LIDAR, tactile sensing, sensor fusion
6. Planning and Decision Making - path planning, motion planning, behavior trees
7. Control Systems - PID control, feedback systems, adaptive control
8. Learning and Adaptation - reinforcement learning, imitation learning, neural networks
9. Human-Robot Interaction - social robotics, natural language processing
10. Applications - healthcare robotics, manufacturing, service robots
11. Ethics and Society - robot ethics, safety, human-robot coexistence
12. Future Directions - emerging technologies, research frontiers

Provide helpful, accurate, and educational responses about robotics and AI. Be friendly and encouraging to learners.
"""

# Fallback responses for when LLM is not available
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

def get_llm_response(message: str) -> str:
    """Get response from Groq LLM with fallback"""
    if not groq_client:
        print("Groq client not available, using fallback")
        return None
    
    try:
        print(f"Sending to LLM: {message}")
        # Try multiple models in order of preference
        models = [
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        ]
        
        for model in models:
            try:
                chat_completion = groq_client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": BOOK_CONTEXT
                        },
                        {
                            "role": "user",
                            "content": message
                        }
                    ],
                    model=model,
                    temperature=0.7,
                    max_tokens=500
                )
                response = chat_completion.choices[0].message.content
                print(f"LLM response from {model}: {response[:100]}...")
                return response
            except Exception as e:
                print(f"Model {model} failed: {str(e)[:100]}")
                continue
        
        print("All models failed")
        return None
    except Exception as e:
        print(f"LLM error: {e}")
        return None

def get_fallback_response(message: str) -> str:
    """Get fallback response when LLM is not available"""
    message_lower = message.lower()
    
    # Determine response category based on keywords
    if any(word in message_lower for word in ['hi', 'hello', 'hey', 'assalam', 'salam']):
        return random.choice(SAMPLE_RESPONSES["greeting"])
        
    elif any(word in message_lower for word in ['walk', 'locomotion', 'gait', 'bipedal', 'balance']):
        return random.choice(SAMPLE_RESPONSES["walking"])
        
    elif any(word in message_lower for word in ['control', 'pid', 'feedback', 'controller']):
        return random.choice(SAMPLE_RESPONSES["control"])
        
    elif any(word in message_lower for word in ['vision', 'camera', 'perception', 'see', 'visual', 'slam']):
        return random.choice(SAMPLE_RESPONSES["vision"])
        
    elif any(word in message_lower for word in ['learn', 'ai', 'machine', 'neural', 'deep', 'algorithm']):
        return random.choice(SAMPLE_RESPONSES["learning"])
        
    elif any(word in message_lower for word in ['design', 'build', 'construct', 'mechanical', 'structure']):
        return random.choice(SAMPLE_RESPONSES["design"])
        
    elif any(word in message_lower for word in ['sensor', 'sensing', 'touch', 'feel', 'detect']):
        return random.choice(SAMPLE_RESPONSES["sensors"])
        
    elif any(word in message_lower for word in ['application', 'use', 'industry', 'healthcare', 'manufacturing']):
        return random.choice(SAMPLE_RESPONSES["applications"])
        
    else:
        return random.choice(SAMPLE_RESPONSES["default"])

@app.get("/")
def read_root():
    return {"message": "Physical AI Textbook API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """Smart chat endpoint with LLM integration"""
    try:
        # Try to get LLM response first
        llm_response = get_llm_response(chat_message.message)
        
        if llm_response:
            return ChatResponse(
                response=llm_response,
                confidence=0.95
            )
        else:
            # Fallback to keyword-based responses
            fallback_response = get_fallback_response(chat_message.message)
            return ChatResponse(
                response=fallback_response,
                confidence=0.7
            )
            
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        return ChatResponse(
            response="I apologize, but I'm experiencing some technical difficulties. Please try asking your question again.",
            confidence=0.5
        )

@app.get("/api/v1/chapters")
def get_chapters():
    """Get list of textbook chapters"""
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)