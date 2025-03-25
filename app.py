import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import plotly.express as px
from datetime import datetime, timedelta
import time

from utils.data_fetcher import fetch_weather_data, get_forest_locations
from utils.visualization import create_temperature_map, plot_temperature_history, create_temperature_gauge

# Set page configuration
st.set_page_config(
    page_title="Forest Temperature Monitor",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application title
st.title("🌲 Forest Temperature Monitoring System")
st.markdown("Monitor forest temperatures to prevent fires and protect wildlife")

# Sidebar for controls
st.sidebar.header("Settings")

# Forest selection
forest_locations = get_forest_locations()
selected_forest = st.sidebar.selectbox(
    "Select Forest Area", 
    options=list(forest_locations.keys())
)

# Refresh rate
refresh_interval = st.sidebar.slider(
    "Data Refresh Interval (minutes)", 
    min_value=5, 
    max_value=60, 
    value=15, 
    step=5
)

# Temperature threshold settings
danger_threshold = st.sidebar.slider(
    "High Temperature Alert Threshold (°C)", 
    min_value=25, 
    max_value=45, 
    value=35
)

warning_threshold = st.sidebar.slider(
    "Warning Temperature Threshold (°C)", 
    min_value=20, 
    max_value=danger_threshold-1, 
    value=30
)

# Fetch the last refresh time from session state or initialize it
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now() - timedelta(minutes=refresh_interval)
    st.session_state.temperature_history = {}
    st.session_state.current_temp_data = None

# Check if it's time to refresh data
current_time = datetime.now()
time_diff = (current_time - st.session_state.last_refresh).total_seconds() / 60

# Force refresh button
if st.sidebar.button("Refresh Data Now"):
    time_diff = refresh_interval  # Force refresh

# Initialize temperature history if not exists
if selected_forest not in st.session_state.temperature_history:
    st.session_state.temperature_history[selected_forest] = []

# Refresh data if needed
if time_diff >= refresh_interval:
    st.session_state.last_refresh = current_time
    
    with st.spinner("Fetching latest temperature data..."):
        # Get coordinates for selected forest
        lat, lon = forest_locations[selected_forest]
        
        # Fetch weather data
        weather_data = fetch_weather_data(lat, lon)
        
        if weather_data:
            st.session_state.current_temp_data = weather_data
            
            # Update temperature history (keep last 24 hours)
            temp_entry = {
                'timestamp': current_time,
                'temperature': weather_data['current_temp'],
                'humidity': weather_data['humidity'],
                'wind_speed': weather_data['wind_speed']
            }
            
            st.session_state.temperature_history[selected_forest].append(temp_entry)
            
            # Keep only last 24 hours of data (assuming 15-minute intervals = 96 points)
            max_history = int(24 * 60 / refresh_interval)
            if len(st.session_state.temperature_history[selected_forest]) > max_history:
                st.session_state.temperature_history[selected_forest] = st.session_state.temperature_history[selected_forest][-max_history:]

# Display the main dashboard in 3 columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"Current Conditions: {selected_forest}")
    
    if st.session_state.current_temp_data:
        data = st.session_state.current_temp_data
        
        # Temperature gauge
        fig = create_temperature_gauge(
            data['current_temp'], 
            warning_threshold, 
            danger_threshold
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Current weather metrics
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            temp_color = (
                "normal" if data['current_temp'] < warning_threshold 
                else "warning" if data['current_temp'] < danger_threshold 
                else "error"
            )
            st.metric(
                "Temperature", 
                f"{data['current_temp']}°C", 
                delta=f"{data['temp_change']:+.1f}°C",
                delta_color=temp_color
            )
        
        with metrics_col2:
            st.metric("Humidity", f"{data['humidity']}%")
        
        with metrics_col3:
            st.metric("Wind Speed", f"{data['wind_speed']} km/h")
            
        # Alert system
        if data['current_temp'] >= danger_threshold:
            st.error(f"⚠️ DANGER: Temperature exceeds critical threshold of {danger_threshold}°C. Fire risk is VERY HIGH!")
        elif data['current_temp'] >= warning_threshold:
            st.warning(f"⚠️ WARNING: Temperature exceeds warning threshold of {warning_threshold}°C. Increased fire risk!")
    else:
        st.info("No temperature data available. Please refresh.")

with col2:
    st.subheader("Map View")
    
    if st.session_state.current_temp_data:
        # Create and display map
        lat, lon = forest_locations[selected_forest]
        temp_data = st.session_state.current_temp_data['current_temp']
        map_fig = create_temperature_map(
            lat, lon, temp_data, 
            warning_threshold, danger_threshold,
            selected_forest
        )
        folium_static(map_fig, width=600, height=400)
    else:
        st.info("Map data unavailable. Please refresh.")

# Historical data section
st.subheader("Temperature History")

if selected_forest in st.session_state.temperature_history and st.session_state.temperature_history[selected_forest]:
    history_data = st.session_state.temperature_history[selected_forest]
    
    # Convert to dataframe for plotting
    history_df = pd.DataFrame(history_data)
    
    # Plot temperature history
    fig = plot_temperature_history(
        history_df, 
        warning_threshold, 
        danger_threshold
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Show raw data table if requested
    if st.checkbox("Show Raw Temperature Data"):
        display_df = history_df.copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(display_df, use_container_width=True)
else:
    st.info("No historical data available yet. Data will appear after multiple refreshes.")

# Footer
st.markdown("---")
st.markdown(
    "**Forest Temperature Monitoring System** - "
    f"Last updated: {st.session_state.last_refresh.strftime('%Y-%m-%d %H:%M:%S')} - "
    f"Next update in: {max(0, refresh_interval - time_diff):.1f} minutes"
)
