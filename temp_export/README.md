# Forest Temperature Monitoring System

A Streamlit web application that monitors temperatures in forest areas to help prevent fires.

## Overview

This project provides real-time temperature monitoring for various forest regions in India, with a focus on fire prevention. The system includes interactive maps, historical temperature tracking, and visual alerts when temperatures approach dangerous levels.

## Features

- **Real-time Temperature Monitoring**: View current temperatures for multiple forest locations
- **Interactive Map**: Visualize forest locations and their temperature status
- **Historical Data**: Track temperature changes over time with animated visualizations
- **Alert System**: Color-coded warnings when temperatures exceed predefined thresholds
- **Customizable Settings**: Adjust refresh rates and temperature thresholds

## Forest Locations Monitored

- Jim Corbett National Park
- Nagarhole National Park
- Bandipur National Park
- Kaziranga National Park
- Sundarbans National Park

## Technical Details

This application is built with:
- Python
- Streamlit
- Pandas
- Folium (for maps)
- Plotly (for interactive charts)

## Getting Started

### Prerequisites
- Python 3.7+
- pip

### Installation

1. Clone this repository:
```bash
git clone https://github.com/PiyushJimiwal/Forest-temperature-monitor.git
cd Forest-temperature-monitor
```

2. Install the required packages:
```bash
pip install -r package_list.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

- Select a forest from the dropdown menu to view its data
- Adjust the temperature thresholds using the sliders
- View historical data using the animated timeline
- Set custom refresh intervals to control data update frequency

## Deployment Options

### Render.com (Recommended)

This repository is configured for easy deployment on Render.com using the `render.yaml` configuration file.

1. Fork or clone this repository to your GitHub account
2. Create a new Web Service on [Render.com](https://render.com/)
3. Connect your GitHub repository
4. Use these settings:
   - **Environment**: Python
   - **Build Command**: `bash render_build.sh`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

The application will automatically deploy using the settings in the `render.yaml` file. For troubleshooting, see the `RENDER_DEPLOYMENT.md` file.

### Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Select this repository
4. Set the main file path to `app.py`
5. Click "Deploy"

### GitHub Pages

This repository can also be deployed to GitHub Pages:

1. Go to your repository Settings → Pages
2. Set the source to GitHub Actions
3. The included workflow will build and deploy the static site

## License

This project is licensed under the MIT License - see the LICENSE file for details.