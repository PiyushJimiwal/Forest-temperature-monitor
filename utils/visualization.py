import folium
from folium.plugins import HeatMap
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_temperature_map(lat, lon, temperature, warning_threshold, danger_threshold, location_name):
    """
    Creates an interactive map with temperature data for the forest location.
    
    Args:
        lat (float): Latitude of the location
        lon (float): Longitude of the location
        temperature (float): Current temperature value
        warning_threshold (float): Temperature threshold for warning alert
        danger_threshold (float): Temperature threshold for danger alert
        location_name (str): Name of the forest location
        
    Returns:
        folium.Map: Interactive map with temperature data
    """
    # Create a map centered at the forest location
    m = folium.Map(location=[lat, lon], zoom_start=10)
    
    # Determine color based on temperature thresholds
    if temperature >= danger_threshold:
        color = 'red'
        temp_status = 'DANGER'
    elif temperature >= warning_threshold:
        color = 'orange'
        temp_status = 'WARNING'
    else:
        color = 'green'
        temp_status = 'NORMAL'
    
    # Add a marker for the forest location with temperature information
    folium.Marker(
        location=[lat, lon],
        popup=f"<strong>{location_name}</strong><br>Temperature: {temperature}°C<br>Status: {temp_status}",
        tooltip=f"{location_name}: {temperature}°C",
        icon=folium.Icon(color=color, icon='thermometer-full', prefix='fa')
    ).add_to(m)
    
    # Create a heat map effect around the location based on temperature
    # Higher temperatures create larger heat zones
    heat_intensity = 1.0 if temperature < warning_threshold else (
        1.5 if temperature < danger_threshold else 2.0
    )
    
    # Generate heat map data points
    heat_data = []
    base_weight = max(0, (temperature - 15) / 5)  # Normalize weight
    
    # Create a grid of points around the forest location for the heat map
    for i in range(-10, 11):
        for j in range(-10, 11):
            # Distance from center point
            distance = (i**2 + j**2) ** 0.5
            if distance <= 10:
                # Weight decreases with distance from center
                weight = base_weight * (1 - distance/10)
                heat_data.append([lat + i * 0.01, lon + j * 0.01, weight * heat_intensity])
    
    # Add heat map to the map
    HeatMap(heat_data, radius=15, blur=10, max_zoom=10).add_to(m)
    
    # Add forest boundary (simplified as a circle)
    folium.Circle(
        location=[lat, lon],
        radius=5000,  # 5km radius
        color='green',
        fill=True,
        fill_opacity=0.1,
        tooltip=f"{location_name} boundary"
    ).add_to(m)
    
    return m

def plot_temperature_history(history_df, warning_threshold, danger_threshold):
    """
    Creates a time series plot of temperature history.
    
    Args:
        history_df (pandas.DataFrame): DataFrame containing temperature history data
        warning_threshold (float): Temperature threshold for warning alert
        danger_threshold (float): Temperature threshold for danger alert
        
    Returns:
        plotly.graph_objects.Figure: Interactive time series plot
    """
    # Create figure
    fig = go.Figure()
    
    # Add temperature line
    fig.add_trace(go.Scatter(
        x=history_df['timestamp'],
        y=history_df['temperature'],
        mode='lines+markers',
        name='Temperature (°C)',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    # Add threshold lines
    fig.add_shape(
        type="line",
        x0=history_df['timestamp'].min(),
        y0=warning_threshold,
        x1=history_df['timestamp'].max(),
        y1=warning_threshold,
        line=dict(color="orange", width=2, dash="dash"),
    )
    
    fig.add_shape(
        type="line",
        x0=history_df['timestamp'].min(),
        y0=danger_threshold,
        x1=history_df['timestamp'].max(),
        y1=danger_threshold,
        line=dict(color="red", width=2, dash="dash"),
    )
    
    # Add annotations
    fig.add_annotation(
        x=history_df['timestamp'].max(),
        y=warning_threshold,
        text="Warning Threshold",
        showarrow=False,
        yshift=10,
        font=dict(color="orange")
    )
    
    fig.add_annotation(
        x=history_df['timestamp'].max(),
        y=danger_threshold,
        text="Danger Threshold",
        showarrow=False,
        yshift=10,
        font=dict(color="red")
    )
    
    # Set chart layout
    fig.update_layout(
        title="Temperature History (Last 24 hours)",
        xaxis_title="Time",
        yaxis_title="Temperature (°C)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    
    # Make sure y-axis covers appropriate temperature range with some padding
    y_min = min(min(history_df['temperature']), warning_threshold) - 5
    y_max = max(max(history_df['temperature']), danger_threshold) + 5
    fig.update_yaxes(range=[y_min, y_max])
    
    return fig

def create_temperature_gauge(temperature, warning_threshold, danger_threshold):
    """
    Creates a gauge chart showing current temperature with color-coded thresholds.
    
    Args:
        temperature (float): Current temperature value
        warning_threshold (float): Temperature threshold for warning alert
        danger_threshold (float): Temperature threshold for danger alert
        
    Returns:
        plotly.graph_objects.Figure: Gauge chart
    """
    # Determine the maximum value for the gauge (at least 10 degrees above the current temperature)
    max_temp = max(50, temperature + 10, danger_threshold + 5)
    
    # Create the gauge figure
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=temperature,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Current Temperature (°C)"},
        gauge={
            'axis': {'range': [0, max_temp]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, warning_threshold], 'color': "lightgreen"},
                {'range': [warning_threshold, danger_threshold], 'color': "orange"},
                {'range': [danger_threshold, max_temp], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': temperature
            }
        }
    ))
    
    # Update layout
    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    
    return fig
