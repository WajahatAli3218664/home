#!/bin/bash

echo "Starting Physical AI Textbook Backend..."

# Navigate to backend directory
cd backend

# Install requirements
echo "Installing Python dependencies..."
pip install -r demo_requirements.txt

# Start the backend server
echo "Starting backend server on port 8000..."
python demo_main.py