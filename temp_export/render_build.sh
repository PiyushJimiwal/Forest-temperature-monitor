#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Installing dependencies for Render deployment..."

# Update pip first
pip install --upgrade pip

# Install core packages one by one - NO folium dependencies!
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install requests==2.31.0
pip install streamlit==1.32.0
pip install plotly==5.18.0
pip install trafilatura==1.6.0

echo "All dependencies installed successfully!"