#!/bin/bash

# Bilimp Terracity Setup Script
# This script sets up the complete environment

echo "=================================="
echo "Bilimp Terracity Setup"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

echo "✓ Docker found"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed"
    exit 1
fi

echo "✓ Docker Compose found"

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created. Please edit it with your configuration."
else
    echo ""
    echo "✓ .env file already exists"
fi

# Start Docker services
echo ""
echo "Starting Docker services (Qdrant and Ollama)..."
docker-compose up -d

echo ""
echo "Waiting for services to be ready..."
sleep 10

# Check if services are running
if docker ps | grep -q bilimp_qdrant; then
    echo "✓ Qdrant is running"
else
    echo "⚠ Warning: Qdrant might not be running"
fi

if docker ps | grep -q bilimp_ollama; then
    echo "✓ Ollama is running"
else
    echo "⚠ Warning: Ollama might not be running"
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Download LLM models:"
echo "   docker exec -it bilimp_ollama ollama pull gemma3:12b"
echo "   docker exec -it bilimp_ollama ollama pull qwen3:9b"
echo ""
echo "2. Place your documents in: data/raw/"
echo ""
echo "3. Process documents:"
echo "   python main.py --mode process --input-dir data/raw"
echo ""
echo "4. Query the system:"
echo "   python main.py --mode query --query 'Your question here'"
echo ""
