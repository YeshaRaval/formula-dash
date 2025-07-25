"""
Graph styling utilities with team colors for F1 Dashboard
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from team_colors import get_all_team_colors, get_team_color

def get_driver_team_color(driver_id, race_id, data):
    """
    Get the team color for a specific driver in a specific race
    
    Args:
        driver_id (int): Driver ID
        race_id (int): Race ID
        data (dict): Data dictionary containing results and constructors
    
    Returns:
        str: Hex color code
    """
    try:
        # Get the constructor for this driver in this race
        race_results = data['results'][
            (data['results']['driverId'] == driver_id) & 
            (data['results']['raceId'] == race_id)
        ]
        
        if not race_results.empty:
            constructor_id = race_results.iloc[0]['constructorId']
            
            # Get constructor reference
            constructor = data['constructors'][data['constructors']['constructorId'] == constructor_id]
            if not constructor.empty:
                constructor_ref = constructor.iloc[0]['constructorRef']
                return get_team_color(constructor_ref)
    except:
        pass
    
    return '#808080'  # Default gray

def get_constructor_color_mapping(data, race_id=None):
    """
    Create a mapping of constructor names to their colors
    
    Args:
        data (dict): Data dictionary
        race_id (int, optional): Specific race ID to filter constructors
    
    Returns:
        dict: Mapping of constructor names to hex colors
    """
    color_mapping = {}
    team_colors = get_all_team_colors()
    
    constructors = data['constructors']
    if race_id:
        # Filter to only constructors in this race
        race_results = data['results'][data['results']['raceId'] == race_id]
        constructor_ids = race_results['constructorId'].unique()
        constructors = constructors[constructors['constructorId'].isin(constructor_ids)]
    
    for _, constructor in constructors.iterrows():
        constructor_name = constructor['name']
        constructor_ref = constructor['constructorRef']
        color_mapping[constructor_name] = team_colors.get(constructor_ref, '#808080')
    
    return color_mapping

def create_styled_bar_chart(df, x, y, color_col, title, x_title=None, y_title=None, data=None, race_id=None):
    """
    Create a bar chart with team colors
    
    Args:
        df (pd.DataFrame): Data for the chart
        x (str): X-axis column name
        y (str): Y-axis column name
        color_col (str): Column to use for coloring (should contain constructor names or driver names)
        title (str): Chart title
        x_title (str, optional): X-axis title
        y_title (str, optional): Y-axis title
        data (dict, optional): Data dictionary for color mapping
        race_id (int, optional): Race ID for color mapping
    
    Returns:
        plotly.graph_objects.Figure: Styled figure
    """
    fig = px.bar(df, x=x, y=y, color=color_col, title=title)
    
    if data and race_id:
        # Apply team colors
        color_mapping = get_constructor_color_mapping(data, race_id)
        
        # Update traces with team colors
        for trace in fig.data:
            trace_name = trace.name
            if trace_name in color_mapping:
                trace.marker.color = color_mapping[trace_name]
    
    fig.update_layout(
        height=500,
        xaxis_title=x_title or x,
        yaxis_title=y_title or y,
        font=dict(size=14),
        showlegend=len(df[color_col].unique()) <= 10  # Only show legend if not too many items
    )
    
    return fig

def create_styled_line_chart(df, x, y, color_col, title, x_title=None, y_title=None, data=None, race_id=None, markers=True):
    """
    Create a line chart with team colors
    
    Args:
        df (pd.DataFrame): Data for the chart
        x (str): X-axis column name
        y (str): Y-axis column name
        color_col (str): Column to use for coloring
        title (str): Chart title
        x_title (str, optional): X-axis title
        y_title (str, optional): Y-axis title
        data (dict, optional): Data dictionary for color mapping
        race_id (int, optional): Race ID for color mapping
        markers (bool): Whether to show markers
    
    Returns:
        plotly.graph_objects.Figure: Styled figure
    """
    fig = px.line(df, x=x, y=y, color=color_col, title=title, markers=markers)
    
    if data and race_id:
        # Apply team colors
        color_mapping = get_constructor_color_mapping(data, race_id)
        
        # Update traces with team colors
        for trace in fig.data:
            trace_name = trace.name
            if trace_name in color_mapping:
                trace.line.color = color_mapping[trace_name]
                if markers:
                    trace.marker.color = color_mapping[trace_name]
    
    fig.update_layout(
        height=500,
        xaxis_title=x_title or x,
        yaxis_title=y_title or y,
        font=dict(size=14)
    )
    
    return fig

def create_styled_pie_chart(df, values, names, title, data=None, race_id=None):
    """
    Create a pie chart with team colors
    
    Args:
        df (pd.DataFrame): Data for the chart
        values (str): Column name for values
        names (str): Column name for names/labels
        title (str): Chart title
        data (dict, optional): Data dictionary for color mapping
        race_id (int, optional): Race ID for color mapping
    
    Returns:
        plotly.graph_objects.Figure: Styled figure
    """
    fig = px.pie(df, values=values, names=names, title=title, hole=0.4)
    
    if data and race_id:
        # Apply team colors
        color_mapping = get_constructor_color_mapping(data, race_id)
        
        # Create color list based on the names
        colors = []
        for name in df[names]:
            colors.append(color_mapping.get(name, '#808080'))
        
        fig.update_traces(marker=dict(colors=colors))
    
    fig.update_layout(
        height=500,
        font=dict(size=14)
    )
    
    return fig

def apply_team_colors_to_existing_chart(fig, df, color_col, data, race_id=None):
    """
    Apply team colors to an existing plotly figure
    
    Args:
        fig (plotly.graph_objects.Figure): Existing figure
        df (pd.DataFrame): Data used in the chart
        color_col (str): Column used for coloring
        data (dict): Data dictionary
        race_id (int, optional): Race ID for color mapping
    
    Returns:
        plotly.graph_objects.Figure: Updated figure with team colors
    """
    if not data or not race_id:
        return fig
    
    # Get driver to constructor mapping for this race
    driver_constructor_mapping = get_driver_constructor_mapping(data, race_id)
    constructor_color_mapping = get_constructor_color_mapping(data, race_id)
    
    # Update traces with team colors
    for trace in fig.data:
        driver_name = trace.name
        if driver_name in driver_constructor_mapping:
            constructor_name = driver_constructor_mapping[driver_name]
            if constructor_name in constructor_color_mapping:
                color = constructor_color_mapping[constructor_name]
                
                # Apply color based on trace type
                if hasattr(trace, 'marker'):
                    trace.marker.color = color
                if hasattr(trace, 'line'):
                    trace.line.color = color
    
    return fig

def get_driver_constructor_mapping(data, race_id):
    """
    Get a mapping of driver names to their constructor names for a specific race
    
    Args:
        data (dict): Data dictionary
        race_id (int): Race ID
    
    Returns:
        dict: Mapping of driver names to constructor names
    """
    mapping = {}
    
    try:
        # Get race results
        race_results = data['results'][data['results']['raceId'] == race_id]
        
        # Merge with driver and constructor data
        results_with_info = race_results.merge(data['drivers'], on='driverId', how='left')
        results_with_info = results_with_info.merge(data['constructors'], on='constructorId', how='left')
        
        for _, row in results_with_info.iterrows():
            driver_name = f"{row['forename']} {row['surname']}"
            constructor_name = row['name']  # Constructor name
            mapping[driver_name] = constructor_name
    except:
        pass
    
    return mapping