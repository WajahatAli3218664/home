# Physical AI & Humanoid Robotics Textbook Platform

Complete interactive learning platform with AI chatbot and comprehensive textbook content.

## 🚀 Quick Start

### One Command Setup

```bash
./start_all.sh
```

This will:
- ✅ Start backend server on port 8000
- ✅ Start frontend on port 3000
- ✅ Open browser automatically

### Manual Setup

**Terminal 1 - Backend:**
```bash
cd backend
python demo_main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## 📋 Prerequisites

- Node.js 20+
- Python 3.12+
- npm

## ✨ Features

### 🤖 AI Chatbot
- **Smart responses** - Understands robotics topics
- **Keyword detection** - Responds to walking, control, vision, AI, sensors, etc.
- **Floating interface** - Available on all pages
- **Real-time chat** - Instant responses

### 📚 Complete Textbook
- 12 comprehensive chapters
- Physical AI fundamentals
- Humanoid robot design
- Control systems
- Machine learning
- Applications

### 🔐 Modern Authentication
- Beautiful login/signup modals
- Social login ready (Google, GitHub)
- Profile management
- Progress tracking

### 👤 Profile Page
- Account information
- Learning goals
- Skill level selection
- Progress statistics

## 🎯 How to Use

1. **Start the platform** - Run `./start_all.sh`
2. **Open browser** - Go to http://localhost:3000
3. **Click chat button** - Floating 💬 button on bottom right
4. **Ask questions** - Type anything about robotics
5. **Sign in** - Click Account → Sign In in navbar

## 💬 Chatbot Topics

The chatbot responds to questions about:
- **Greetings**: hi, hello, hey
- **Walking**: locomotion, gait, bipedal, balance
- **Control**: PID, feedback, controllers
- **Vision**: cameras, perception, SLAM
- **AI/Learning**: machine learning, neural networks
- **Design**: robot construction, mechanics
- **Sensors**: touch, detection, sensing
- **Applications**: healthcare, manufacturing

## 🔧 Troubleshooting

### Backend not responding
```bash
pkill -f "python demo_main.py"
cd backend && python demo_main.py
```

### Frontend errors
```bash
cd frontend
npm install
npm start
```

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

## 📁 Project Structure

```
├── backend/
│   ├── demo_main.py          # Main backend server
│   ├── demo_requirements.txt # Python dependencies
│   └── backend.log           # Server logs
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── LoginForm.jsx
│   │   │   └── SignupForm.jsx
│   │   └── pages/
│   │       └── profile.jsx
│   └── docs/                 # Textbook chapters
├── start_all.sh              # Combined startup script
└── README.md
```

## 🌐 API Endpoints

- `GET /` - Health check
- `GET /health` - Backend status
- `POST /api/v1/chat` - Chat with AI
- `GET /api/v1/chapters` - Get chapters list

## 📝 Environment Variables

Create `.env` file in root:
```
GROQ_API_KEY=your_key_here
REACT_APP_API_BASE_URL=http://localhost:8000
```

## 🎨 Tech Stack

- **Frontend**: Docusaurus, React, TypeScript
- **Backend**: FastAPI, Python
- **Styling**: CSS3, Modern animations
- **AI**: Context-aware responses

## ✅ Verified Working

- ✅ Backend server running
- ✅ Chatbot responding correctly
- ✅ Authentication modals working
- ✅ Profile page functional
- ✅ All UI components styled
- ✅ Mobile responsive

## 🚀 Deployment Ready

Backend and frontend are ready for deployment on:
- Vercel (Frontend)
- Railway/Render (Backend)
- GitHub Pages (Static)

---

**Made with ❤️ for Physical AI Education**

For issues or questions, check the logs:
- Backend: `backend/backend.log`
- Frontend: Browser console (F12)