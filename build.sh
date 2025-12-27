#!/bin/bash
# Build script for Vercel deployment

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Go back to root
cd ..

# Install frontend dependencies and build
cd frontend
npm install
npm run build