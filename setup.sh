#!/bin/bash
# Solar Sentinel AI - macOS/Linux Setup Script
# Installs dependencies and prepares the application

echo ""
echo "======================================"
echo "  Solar Sentinel AI - Setup"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[1/4] Python version check... OK"
python3 --version

echo ""
echo "[2/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[3/4] Activating virtual environment..."
source venv/bin/activate

echo "[4/4] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "======================================"
echo "  ✓ Setup Complete!"
echo "======================================"
echo ""
echo "To start the application, run:"
echo "  streamlit run app.py"
echo ""
echo "The app will open at: http://localhost:8501"
echo ""
