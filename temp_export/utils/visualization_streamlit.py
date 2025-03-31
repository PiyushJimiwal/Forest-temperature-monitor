import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_plotly_map(lat, lon, temperature, warning_threshold, danger_threshold, location_name):
    """
    Creates an interactive map with temperature data for the forest location using Plotly.
    This replaces the folium-based map with a pure Plotly solution.
    
    Args:
        lat (float): Latitude of the location
        lon (float): Longitude of the location
        temperature (float): Current temperature value
        warning_threshold (float): Temperature threshold for warning alert
        danger_threshold (float): Temperature threshold for danger alert
        location_name (str): Name of the forest location
        
    Returns:
        plotly.graph_objects.Figure: Interactive plotly map with temperature data
    """
    # Determine marker color based on temperature thresholds
    if temperature >= danger_threshold:
        color = 'red'
        temp_status = 'DANGER'
    elif temperature >= warning_threshold:
        color = 'orange'
        temp_status = 'WARNING'
    else:
        color = 'green'
        temp_status = 'NORMAL'
    
    # Create a dataframe with the location
    df = pd.DataFrame({
        'lat': [lat],
        'lon': [lon],
        'name': [location_name],
        'temperature': [temperature],
        'status': [temp_status]
    })
    
    # Create the map
    fig = px.scatter_mapbox(
        df, 
        lat='lat', 
        lon='lon',
        hover_name='name',
        hover_data={'temperature': True, 'status': True, 'lat': False, 'lon': False},
        color_discrete_sequence=[color],
        zoom=9,
        height=400,
    )
    
    # Add forest boundary (as a circle on the map)
    # Generate points for a circle around the forest location
    circle_points = []
    for angle in range(0, 360, 10):
        angle_rad = angle * np.pi / 180
        # Approximate 5km radius in degrees (very rough approximation)
        radius_deg = 5 / 111  # 1 degree is approximately 111 km
        circle_lat = lat + radius_deg * np.sin(angle_rad)
        circle_lon = lon + radius_deg * np.cos(angle_rad)
        circle_points.append((circle_lat, circle_lon))
    
    # Extract circle coordinates
    circle_lats = [p[0] for p in circle_points]
    circle_lons = [p[1] for p in circle_points]
    
    # Add the circle as a line on the map
    fig.add_trace(go.Scattermapbox(
        lat=circle_lats,
        lon=circle_lons,
        mode='lines',
        line=dict(width=2, color='green'),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Configure mapbox
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(
            center=dict(lat=lat, lon=lon),
            zoom=9
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        height=400,
    )
    
    return fig

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
    
    # Create the gauge figure with animation
    fig = go.Figure()
    
    # Add animated trace that goes from 0 to the actual temperature
    for i in range(0, int(temperature) + 1, max(1, int(temperature // 10))):
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=i,
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
                        'value': i
                    }
                },
                visible=False
            )
        )
    
    # Add the final gauge with the actual temperature
    fig.add_trace(
        go.Indicator(
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
        )
    )
    
    # Create frames for animation
    frames = []
    for i in range(len(fig.data)):
        frame_data = []
        for j in range(len(fig.data)):
            visible = True if j == i else False
            frame_data.append(go.Indicator(visible=visible))
        frames.append(go.Frame(data=frame_data, name=str(i)))
    
    fig.frames = frames
    
    # Add animation buttons
    fig.update_layout(
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [{
                'label': 'Play',
                'method': 'animate',
                'args': [None, {'frame': {'duration': 50, 'redraw': True}, 'fromcurrent': True}]
            }],
            'x': 0.1,
            'y': 0,
        }],
        height=300,
        margin=dict(l=10, r=10, t=50, b=50),
    )
    
    return fig

def add_animated_icon(temperature):
    """
    Creates an animated icon based on the temperature level.
    
    Args:
        temperature (float): Current temperature value
        
    Returns:
        str: HTML for the animated icon
    """
    # Generate a simple CSS animation based on temperature
    # Higher temperature = faster animation
    animation_speed = max(1, min(5, temperature / 10))  # Scale between 1-5 seconds
    
    if temperature >= 35:  # High temperature - fire icon
        icon_color = "red"
        icon_name = "fire"
        animation = f"""
        @keyframes pulse-{icon_name} {{
            0% {{ transform: scale(1); opacity: 0.8; }}
            50% {{ transform: scale(1.2); opacity: 1; }}
            100% {{ transform: scale(1); opacity: 0.8; }}
        }}
        """
        animation_style = f"animation: pulse-{icon_name} {animation_speed}s infinite;"
    
    elif temperature >= 25:  # Medium temperature - thermometer icon
        icon_color = "orange"
        icon_name = "thermometer-three-quarters"
        animation = f"""
        @keyframes shake-{icon_name} {{
            0% {{ transform: rotate(0deg); }}
            25% {{ transform: rotate(5deg); }}
            50% {{ transform: rotate(0deg); }}
            75% {{ transform: rotate(-5deg); }}
            100% {{ transform: rotate(0deg); }}
        }}
        """
        animation_style = f"animation: shake-{icon_name} {animation_speed}s infinite;"
    
    else:  # Low temperature - normal thermometer
        icon_color = "green"
        icon_name = "thermometer-quarter"
        animation = f"""
        @keyframes fade-{icon_name} {{
            0% {{ opacity: 0.7; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.7; }}
        }}
        """
        animation_style = f"animation: fade-{icon_name} {animation_speed*2}s infinite;"
    
    # Generate the HTML with embedded CSS animation
    html = f"""
    <style>
        {animation}
        .animated-icon-{icon_name} {{
            display: inline-block;
            {animation_style}
            color: {icon_color};
            font-size: 3rem;
        }}
    </style>
    <div class="animated-icon-{icon_name}">
        <i class="fas fa-{icon_name}"></i>
    </div>
    """
    
    return html