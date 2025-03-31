#!/bin/bash

# Stop on errors
set -e

echo "Installing dependencies..."

# Clear pip cache to avoid issues
pip cache purge

# Uninstall conflicting packages first
pip uninstall -y streamlit-folium folium

# Install specific versions one by one to avoid conflicts
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install requests==2.31.0
pip install streamlit==1.32.0
pip install folium==0.14.0
pip install plotly==5.18.0
pip install trafilatura==1.6.0

# Install streamlit-folium last to avoid conflicts
pip install streamlit-folium==0.15.0 --no-deps

echo "Dependencies installed successfully!"