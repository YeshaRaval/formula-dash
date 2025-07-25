"""
Card styling utilities with team color borders for F1 Dashboard
"""

import streamlit as st
import pandas as pd
from team_colors import get_all_team_colors, get_team_color
from utils import get_constructor_name

def get_driver_team_color_for_race(driver_id, race_id, data):
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

def create_team_colored_card(content, team_color, border_color=None, text_color="#000000"):
    """
    Create a card with neutral background and team color border
    
    Args:
        content (str): HTML content for the card
        team_color (str): Border color hex code
        border_color (str, optional): Border color hex code
        text_color (str): Text color hex code (default black)
    
    Returns:
        str: HTML string for the card
    """
    if not border_color:
        border_color = team_color
    
    # Use neutral background that works in both light and dark mode
    background_color = "#f8f9fa"  # Light neutral background
    
    return f"""
    <div style="background-color:{background_color}; border:3px solid {border_color}; border-radius:10px; padding:20px; text-align:center; margin-bottom:10px;">
        <div style="color:{text_color};">
            {content}
        </div>
    </div>
    """

def create_race_winner_card(driver_name, driver_number, race_time, team_color):
    """Create race winner card with team color border"""
    content = f"""
        <div style="font-size:40px; margin-bottom:10px;">🏆</div>
        <h4 style="margin:0; font-weight:bold; font-size:16px;">Race Winner</h4>
        <h3 style="margin:10px 0; font-weight:bold; font-size:18px;">{driver_number} {driver_name}</h3>
        <p style="margin:0; font-size:14px;">{race_time}</p>
    """
    return create_team_colored_card(content, team_color)

def create_pole_position_card(driver_name, driver_number, quali_time, team_color):
    """Create pole position card with team color border"""
    content = f"""
        <div style="font-size:40px; margin-bottom:10px;">🥇</div>
        <h4 style="margin:0; font-weight:bold; font-size:16px;">Pole Position</h4>
        <h3 style="margin:10px 0; font-weight:bold; font-size:18px;">{driver_number} {driver_name}</h3>
        <p style="margin:0; font-size:14px;">{quali_time}</p>
    """
    return create_team_colored_card(content, team_color)

def create_fastest_lap_card(driver_name, driver_number, lap_time, team_color):
    """Create fastest lap card with team color border"""
    content = f"""
        <div style="font-size:40px; margin-bottom:10px;">⚡</div>
        <h4 style="margin:0; font-weight:bold; font-size:16px;">Fastest Lap</h4>
        <h3 style="margin:10px 0; font-weight:bold; font-size:18px;">{driver_number} {driver_name}</h3>
        <p style="margin:0; font-size:14px;">{lap_time}</p>
    """
    return create_team_colored_card(content, team_color)

def create_sprint_podium_card(position, driver_name, driver_number, race_time, team_color):
    """Create sprint podium card with team color border"""
    position_info = {
        1: {"emoji": "🏆", "title": "Sprint Winner"},
        2: {"emoji": "🥈", "title": "2nd Place"},
        3: {"emoji": "🥉", "title": "3rd Place"}
    }
    
    info = position_info.get(position, {"emoji": "🏁", "title": f"{position}th Place"})
    
    content = f"""
        <div style="font-size:40px; margin-bottom:10px;">{info['emoji']}</div>
        <h4 style="margin:0; font-weight:bold; font-size:16px;">{info['title']}</h4>
        <h3 style="margin:10px 0; font-weight:bold; font-size:18px;">{driver_number} {driver_name}</h3>
        <p style="margin:0; font-size:14px;">{race_time}</p>
    """
    return create_team_colored_card(content, team_color)

def create_qualifying_session_best_card(session, driver_name, driver_number, time_formatted, team_color):
    """Create qualifying session best time card with team color border"""
    content = f"""
        <h4 style="margin-top:0; margin-bottom:8px; font-weight:bold; font-size:18px;">Best {session} Time</h4>
        <h3 style="margin:5px 0; font-weight:bold; font-size:22px;">{driver_number} {driver_name}</h3>
        <p style="margin-bottom:0; font-size:18px;">{time_formatted}</p>
    """
    return f"""
    <div style="background-color:#f8f9fa; border:3px solid {team_color}; border-radius:10px; padding:15px; text-align:left;">
        <div style="color:#000000;">
            {content}
        </div>
    </div>
    """

def create_qualifying_comparison_card(driver_name, driver_number, time_formatted, session, team_color):
    """Create qualifying comparison card with team color border"""
    content = f"""
        <h4 style="margin-top:0; margin-bottom:8px; font-weight:bold; font-size:18px;">{driver_number} {driver_name}</h4>
        <h3 style="margin:5px 0; font-weight:bold; font-size:24px;">{time_formatted}</h3>
        <p style="margin-bottom:0; font-size:18px;">{session}</p>
    """
    return f"""
    <div style="background-color:#f8f9fa; border:3px solid {team_color}; border-radius:10px; padding:15px; text-align:left;">
        <div style="color:#000000;">
            {content}
        </div>
    </div>
    """

def create_starting_grid_card_with_team_color(position, driver_name, team_name, driver_number, team_color):
    """Create starting grid card with team color border"""
    number_display = f"#{driver_number}" if driver_number and str(driver_number) != 'nan' else ""
    
    content = f"""
        <div style="position: absolute; top: 10px; left: 10px; background: #ff0000; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 16px;">{position}</div>
        <div style="margin-top: 20px;">
            <div style="font-size: 18px; font-weight: bold; margin-bottom: 5px;">{number_display}</div>
            <div style="font-size: 22px; font-weight: bold; margin: 8px 0;">{driver_name}</div>
            <div style="font-size: 16px; margin-top: 5px;">{team_name}</div>
        </div>
    """
    
    return f"""
    <div style="background: #f8f9fa; border: 3px solid {team_color}; border-radius: 12px; padding: 15px; margin: 8px 0; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: transform 0.2s ease; position: relative;">
        <div style="color: #000000;">
            {content}
        </div>
    </div>
    """