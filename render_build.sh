#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Installing dependencies for Render deployment..."

# Update pip first
pip install --upgrade pip

# Uninstall any conflicting packages
pip uninstall -y streamlit-folium || true
pip uninstall -y folium || true

# Install core packages one by one
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install requests==2.31.0
pip install streamlit==1.32.0
pip install plotly==5.18.0
pip install trafilatura==1.6.0

# Install folium and streamlit-folium separately with no dependencies
pip install folium==0.14.0 --no-deps
pip install streamlit-folium==0.15.0 --no-deps

# Install branca (required by folium)
pip install branca==0.6.0

# Install jinja2 (required by folium)
pip install jinja2==3.1.2

echo "All dependencies installed successfully!"