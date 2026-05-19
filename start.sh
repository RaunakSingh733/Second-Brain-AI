#!/bin/bash

# Second Brain AI - Quick Start Script
# This script sets up and runs Second Brain AI locally

set -e

echo "🧠 Second Brain AI - Quick Start"
echo "=================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "\n${BLUE}Checking prerequisites...${NC}"

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.9+"
    exit 1
fi
echo "✅ Python found: $(python --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install Ollama from https://ollama.ai"
    exit 1
fi
echo "✅ Ollama found"

# Setup Backend
echo -e "\n${BLUE}Setting up backend...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
echo "✅ Backend dependencies installed"

# Setup Frontend
echo -e "\n${BLUE}Setting up frontend...${NC}"
cd ../frontend

npm install
echo "✅ Frontend dependencies installed"

echo -e "\n${GREEN}✅ Setup complete!${NC}"
echo ""
echo "To start the application:"
echo "1. Start backend: cd backend && uvicorn main:app --reload"
echo "2. Start frontend: cd frontend && npm run dev"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "Make sure Ollama is running: ollama serve"
echo "And pull a model: ollama pull qwen:7b"
