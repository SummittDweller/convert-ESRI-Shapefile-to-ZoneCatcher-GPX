#!/bin/bash

# Script to manage virtual environment and run main.py

# Navigate to the script's directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating .venv..."
    python3 -m venv .venv
    if [ $? -eq 0 ]; then
        echo "Virtual environment created successfully."
    else
        echo "Failed to create virtual environment."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if python-requirements.txt exists and install dependencies
if [ -f "python-requirements.txt" ]; then
    echo "Installing dependencies from python-requirements.txt..."
    pip install -r python-requirements.txt
fi

# Run the Python script
echo "Running main.py..."
python main.py
