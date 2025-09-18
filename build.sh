#!/bin/bash
# Build script for Render deployment

# Set Python version
export PYTHON_VERSION=3.11.9

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p outputs uploads temp
