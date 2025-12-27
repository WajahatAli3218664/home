import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEXT_OPTIONS = [
    "Welcome to the Physical AI & Humanoid Robotics Textbook!",
    "Advanced robotics combines mechanical engineering, electrical engineering, and computer science.",
    "Machine learning algorithms enable robots to adapt to new environments.",
    "Humanoid robots represent one of the most challenging areas in robotics research.",
    "Kinematics and dynamics are fundamental concepts in robot motion planning.",
    "Artificial intelligence is revolutionizing the capabilities of autonomous systems.",
    "Sensor fusion allows robots to perceive their environment accurately.",
    "Control theory provides the mathematical foundation for robotic movement.",
    "Computer vision enables robots to interpret visual information from cameras.",
    "Natural language processing allows humans to interact with robots using speech."
]

@app.get("/")
def read_root():
    return {"message": "Text Generator API is running on port 3000!"}

@app.get("/generate-text")
def generate_text():
    """Generate a random text related to robotics and AI"""
    text = random.choice(TEXT_OPTIONS)
    return {"text": text}

@app.get("/generate-text-multiple")
def generate_text_multiple(count: int = 5):
    """Generate multiple random texts related to robotics and AI"""
    texts = [random.choice(TEXT_OPTIONS) for _ in range(min(count, 10))]  # Limit to 10
    return {"texts": texts}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("text_generator:app", host="0.0.0.0", port=3000, reload=True)