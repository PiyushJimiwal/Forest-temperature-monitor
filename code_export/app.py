import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import base64

from utils.data_fetcher import fetch_weather_data, get_forest_locations
from utils.visualization_streamlit import create_plotly_map, plot_temperature_history, create_temperature_gauge, add_animated_icon

# Set page configuration
st.set_page_config(
    page_title="Forest Temperature Monitor",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add Font Awesome to enable icons
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# Application title with animated header
st.markdown("""
<style>
@keyframes color-change {
    0% { color: #2E8B57; }  /* Forest green */
    50% { color: #FF4500; } /* Orange red */
    100% { color: #2E8B57; }
}

.animated-title {
    font-size: 2.5rem;
    font-weight: bold;
    animation: color-change 5s infinite;
    padding: 0.5rem 0;
}
</style>
<div class="animated-title">🌲 Forest Temperature Monitoring System</div>
""", unsafe_allow_html=True)

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
            
        # Alert system with animated icons
        if data['current_temp'] >= danger_threshold:
            alert_col1, alert_col2 = st.columns([1, 3])
            with alert_col1:
                st.markdown(add_animated_icon(data['current_temp']), unsafe_allow_html=True)
            with alert_col2:
                st.error(f"DANGER: Temperature exceeds critical threshold of {danger_threshold}°C. Fire risk is VERY HIGH!")
        elif data['current_temp'] >= warning_threshold:
            alert_col1, alert_col2 = st.columns([1, 3])
            with alert_col1:
                st.markdown(add_animated_icon(data['current_temp']), unsafe_allow_html=True)
            with alert_col2:
                st.warning(f"WARNING: Temperature exceeds warning threshold of {warning_threshold}°C. Increased fire risk!")
    else:
        st.info("No temperature data available. Please refresh.")

with col2:
    st.subheader("Map View")
    
    if st.session_state.current_temp_data:
        # Create and display map
        lat, lon = forest_locations[selected_forest]
        temp_data = st.session_state.current_temp_data['current_temp']
        map_fig = create_plotly_map(
            lat, lon, temp_data, 
            warning_threshold, danger_threshold,
            selected_forest
        )
        st.plotly_chart(map_fig, use_container_width=True)
    else:
        st.info("Map data unavailable. Please refresh.")

# Historical data section with animation
st.markdown("""
<style>
@keyframes slide-in {
    0% { transform: translateX(-100%); opacity: 0; }
    100% { transform: translateX(0); opacity: 1; }
}
.animated-header {
    animation: slide-in 1.5s ease-out;
}
</style>
<div class="animated-header">
    <h3>Temperature History</h3>
</div>
""", unsafe_allow_html=True)

if selected_forest in st.session_state.temperature_history and st.session_state.temperature_history[selected_forest]:
    history_data = st.session_state.temperature_history[selected_forest]
    
    # Convert to dataframe for plotting
    history_df = pd.DataFrame(history_data)
    
    # Plot temperature history with animation
    fig = plot_temperature_history(
        history_df, 
        warning_threshold, 
        danger_threshold
    )
    
    # Add frame-by-frame animation to the plot
    frames = []
    for i in range(1, len(history_df) + 1):
        subset = history_df.iloc[:i]
        if not subset.empty:
            frame_fig = go.Frame(
                data=[go.Scatter(
                    x=subset['timestamp'], 
                    y=subset['temperature'],
                    mode='lines+markers',
                    line=dict(color='#1f77b4', width=3),
                    marker=dict(size=6)
                )],
                name=f"frame{i}"
            )
            frames.append(frame_fig)
    
    if frames:
        fig.frames = frames
        fig.update_layout(
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [{
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True}]
                }],
                'x': 0.1,
                'y': 0
            }]
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show raw data table if requested
    if st.checkbox("Show Raw Temperature Data"):
        display_df = history_df.copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(display_df, use_container_width=True)
else:
    st.info("No historical data available yet. Data will appear after multiple refreshes.")

# FAQ Section
st.markdown("---")
st.subheader("Frequently Asked Questions")

with st.expander("What is the purpose of this monitoring system?"):
    st.write("""
    The Forest Temperature Monitoring System tracks temperature changes in key Indian forest areas to:
    - Detect potential fire risks by monitoring temperature spikes
    - Provide early warnings to forest management authorities
    - Track historical temperature patterns for forest health assessment
    - Support conservation efforts for forest wildlife and ecosystems
    """)

with st.expander("How does the temperature alert system work?"):
    st.write("""
    The system uses two threshold levels:
    - **Warning level** (customizable, default 30°C): Indicates elevated temperature that requires attention
    - **Danger level** (customizable, default 35°C): Indicates critical temperature with high fire risk
    
    When temperatures exceed these thresholds, the system displays visual alerts with animated icons and color-coded warnings.
    """)

with st.expander("Which Indian forests are monitored?"):
    st.write("""
    The system currently monitors five key Indian forest regions:
    1. **Jim Corbett National Park** - Uttarakhand, famous for tigers and elephants
    2. **Nagarhole National Park** - Karnataka, part of the Nilgiri Biosphere Reserve
    3. **Bandipur National Park** - Karnataka, known for its dry deciduous forests
    4. **Kaziranga National Park** - Assam, home to two-thirds of the world's great one-horned rhinoceroses
    5. **Sundarbans** - West Bengal, the largest mangrove forest in the world
    """)

with st.expander("How accurate is the temperature data?"):
    st.write("""
    The temperature data comes from deterministic algorithms that simulate real-world patterns based on:
    - Geographic location (latitude/longitude)
    - Time of day temperature cycles
    - Historical weather patterns for the region
    
    This approach ensures consistent and realistic temperature patterns for demonstration purposes.
    """)

# Animated Footer
st.markdown("---")

# Calculate percentage of time elapsed until next update
time_remaining = max(0, refresh_interval - time_diff)
progress_percent = 100 - (time_remaining / refresh_interval * 100)

# Create an animated progress bar for the time until next update
footer_html = f"""
<style>
@keyframes pulse {{
    0% {{ opacity: 0.7; }}
    50% {{ opacity: 1; }}
    100% {{ opacity: 0.7; }}
}}

.footer-container {{
    margin-top: 20px;
    padding: 10px;
    border-radius: 5px;
    background-color: #f0f0f0;
}}

.update-progress {{
    height: 5px;
    background-color: #dcdcdc;
    border-radius: 5px;
    margin-top: 10px;
    position: relative;
}}

.update-progress-bar {{
    height: 100%;
    width: {progress_percent}%;
    background-color: #2E8B57;
    border-radius: 5px;
    animation: pulse 2s infinite;
}}

.footer-text {{
    margin-bottom: 5px;
    font-weight: bold;
}}

.time-info {{
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: #666;
}}
</style>

<div class="footer-container">
    <div class="footer-text">Forest Temperature Monitoring System</div>
    <div>Last updated: {st.session_state.last_refresh.strftime('%Y-%m-%d %H:%M:%S')} - Next update in: {time_remaining:.1f} minutes</div>
    <div class="update-progress">
        <div class="update-progress-bar"></div>
    </div>
    <div class="time-info">
        <span>Just updated</span>
        <span>Next update</span>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
