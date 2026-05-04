#!/bin/bash

# Update package lists and upgrade packages
sudo apt update
sudo apt upgrade -y

# Create virtual environment with access to system packages
python3 -m venv --system-site-packages .venv

# Activate virtual environment
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install ffmpeg
# Ubuntu/Debian:
sudo apt install ffmpeg -y
