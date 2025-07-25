"""Utility functions for F1 dashboard"""

import pandas as pd
from datetime import datetime

def race_has_sprint(race_id):
    """Check if a race has sprint data"""
    try:
        # Try to load sprint results data
        sprint_data = pd.read_csv('f1_data/sprint_results.csv')
        sprint_results = sprint_data[sprint_data['raceId'] == race_id]
        return not sprint_results.empty
    except Exception:
        return False

def time_to_seconds(time_str):
    """Convert time string to seconds"""
    if pd.isna(time_str) or time_str == '':
        return None
    
    try:
        if ':' in time_str:
            parts = time_str.split(':')
            minutes = float(parts[0])
            seconds = float(parts[1])
            return minutes * 60 + seconds
        else:
            return float(time_str)
    except:
        return None

def format_time_mmssms(seconds):
    """Format seconds as MM:SS.ms"""
    if seconds is None:
        return "N/A"
    
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:.3f}"

def get_constructor_name(row, data):
    """Get constructor name from row data"""
    try:
        # First try to use merged constructor name (from constructor table)
        if 'name_y' in row.index and pd.notna(row['name_y']):
            return row['name_y']
        elif 'name' in row.index and pd.notna(row['name']):
            # Make sure it's not a driver name
            driver_name = f"{row.get('forename', '')} {row.get('surname', '')}".strip()
            if row['name'] != driver_name:
                return row['name']
        
        # Fallback: lookup constructor by ID
        if 'constructorId' in row.index and pd.notna(row['constructorId']):
            constructor = data['constructors'][data['constructors']['constructorId'] == row['constructorId']]
            if not constructor.empty:
                return constructor.iloc[0]['name']
        
        return 'N/A'
    except:
        return 'N/A'

def format_race_date(date_str):
    """Format date as 'Date of the Race : 3rd August 2024' style"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day = date_obj.day
        
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        
        return f"Date of the Race : {day}{suffix} {date_obj.strftime('%B %Y')}"
    except:
        return f"Date of the Race : {date_str}"

def calculate_gap_to_leader(row, winner_milliseconds):
    """Calculate gap to race leader"""
    try:
        if pd.notna(row['milliseconds']) and row['milliseconds'] > 0:
            gap_ms = row['milliseconds'] - winner_milliseconds
            gap_seconds = gap_ms / 1000
            return f"+{gap_seconds:.3f}s"
        elif pd.notna(row['time']) and row['time'] != '':
            return row['time']
        else:
            return ""
    except:
        return ""