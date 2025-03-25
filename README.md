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
git clone https://github.com/yourusername/forest-temperature-monitor.git
cd forest-temperature-monitor
```

2. Install the required packages:
```bash
pip install -r requirements.txt
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

## License

This project is licensed under the MIT License - see the LICENSE file for details.