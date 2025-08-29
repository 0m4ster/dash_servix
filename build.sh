#!/bin/bash
set -e

echo "Setting Python version..."
python --version

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing numpy first..."
pip install "numpy>=1.24.0,<2.0.0"

echo "Installing pandas..."
pip install pandas==2.2.0

echo "Installing remaining requirements..."
pip install -r requirements.txt

echo "Build completed successfully!"
