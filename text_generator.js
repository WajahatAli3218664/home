const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 3000;

// Enable CORS for all routes
app.use(cors());

// Sample text options
const TEXT_OPTIONS = [
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
];

// Root endpoint
app.get('/', (req, res) => {
  res.json({ message: "Text Generator API is running on port 3000!" });
});

// Generate single text endpoint
app.get('/generate-text', (req, res) => {
  const randomIndex = Math.floor(Math.random() * TEXT_OPTIONS.length);
  const text = TEXT_OPTIONS[randomIndex];
  res.json({ text });
});

// Generate multiple texts endpoint
app.get('/generate-text-multiple', (req, res) => {
  const count = parseInt(req.query.count) || 5;
  const validCount = Math.min(Math.max(count, 1), 10); // Between 1 and 10
  const texts = [];
  
  for (let i = 0; i < validCount; i++) {
    const randomIndex = Math.floor(Math.random() * TEXT_OPTIONS.length);
    texts.push(TEXT_OPTIONS[randomIndex]);
  }
  
  res.json({ texts });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Text Generator server running on port ${PORT}`);
});