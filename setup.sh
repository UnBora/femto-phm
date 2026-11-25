#!/bin/bash

# FEMTO-PHM Environment Setup Script
# Run with: bash setup.sh

echo "======================================"
echo "FEMTO-PHM Environment Setup"
echo "======================================"

# Check Python version
echo "Checking Python..."
python3 --version

# Option 1: Using system pip (if available)
echo ""
echo "Option 1: Installing system-wide with pip..."
python3 -m pip install --user -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully!"
    exit 0
fi

# Option 2: Try apt-get if pip fails
echo ""
echo "Option 2: Trying apt-get..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv
python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully!"
    exit 0
fi

# Option 3: Virtual environment (if venv is available)
echo ""
echo "Option 3: Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Virtual environment created and dependencies installed!"
    echo "To activate: source venv/bin/activate"
    exit 0
fi

echo "❌ Installation failed. Please try one of the following:"
echo ""
echo "1. Manual pip installation:"
echo "   python3 -m pip install --user numpy pandas matplotlib seaborn scikit-learn scipy jupyter ipython"
echo ""
echo "2. Using apt (Debian/Ubuntu):"
echo "   sudo apt-get install python3-pip python3-venv"
echo "   python3 -m pip install -r requirements.txt"
echo ""
echo "3. Using conda/mamba:"
echo "   conda create -n femto-phm --file requirements.txt"
echo "   conda activate femto-phm"
