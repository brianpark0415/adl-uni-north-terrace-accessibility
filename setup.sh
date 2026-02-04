#!/bin/bash

echo "==================================="
echo "Accessible Campus Navigation Setup"
echo "==================================="

# Check Python version
echo -e "\n1. Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    echo "✓ Python 3 found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    echo "✓ Python found: $(python --version)"
else
    echo "✗ Python not found. Please install Python 3.8+"
    exit 1
fi

# Check pip
echo -e "\n2. Checking pip installation..."
if command -v pip3 &> /dev/null; then
    PIP_CMD=pip3
    echo "✓ pip3 found"
elif command -v pip &> /dev/null; then
    PIP_CMD=pip
    echo "✓ pip found"
else
    echo "✗ pip not found. Installing pip..."
    $PYTHON_CMD -m ensurepip --upgrade
    PIP_CMD="$PYTHON_CMD -m pip"
fi

# Create virtual environment
echo -e "\n3. Creating virtual environment..."
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo -e "\n4. Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✓ Virtual environment activated"

# Install dependencies
echo -e "\n5. Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Run demo
echo -e "\n6. Running demo to verify installation..."
python demo.py

echo -e "\n==================================="
echo "Setup complete!"
echo "==================================="
echo -e "\nTo start the web server:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate  (Mac/Linux)"
echo "     venv\\Scripts\\activate     (Windows)"
echo "  2. Run: python app.py"
echo "  3. Open: http://localhost:5000"
echo ""
