"""Data loading utilities for F1 Dashboard with Local Images"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

@st.cache_data
def load_data():
    """Load all F1 data files with local images"""
    data = {}
    try:
        # Check if local images CSV exists, otherwise use original
        local_images_file = 'f1_data/circuits_with_local_images.csv'
        original_file = 'f1_data/circuits_updated.csv'
        
        if os.path.exists(local_images_file):
            circuits_file = local_images_file
        else:
            circuits_file = original_file
        
        # Get file modification time for cache invalidation
        file_mod_time = os.path.getmtime(circuits_file) if os.path.exists(circuits_file) else 0
        
        data['races'] = pd.read_csv('f1_data/races.csv')
        data['circuits'] = pd.read_csv(circuits_file)
        data['results'] = pd.read_csv('f1_data/results.csv')
        data['drivers'] = pd.read_csv('f1_data/drivers.csv')
        data['constructors'] = pd.read_csv('f1_data/constructors.csv')
        
        # Handle driver standings with special care for invalid values
        try:
            # Read driver standings with appropriate NA values
            driver_standings = pd.read_csv('f1_data/driver_standings.csv', na_values=['\\N', 'N'])
            
            # Convert problematic columns to appropriate types
            for col in ['position', 'points', 'wins']:
                if col in driver_standings.columns:
                    driver_standings[col] = pd.to_numeric(driver_standings[col], errors='coerce')
            
            data['driver_standings'] = driver_standings
        except Exception as e:
            st.warning(f"Driver standings data may have issues: {e}")
        
        # Handle constructor standings with special care for invalid values
        try:
            # Read constructor standings with appropriate NA values
            constructor_standings = pd.read_csv('f1_data/constructor_standings.csv', na_values=['\\N', 'N'])
            
            # Convert problematic columns to appropriate types
            for col in ['position', 'points', 'wins']:
                if col in constructor_standings.columns:
                    constructor_standings[col] = pd.to_numeric(constructor_standings[col], errors='coerce')
            
            data['constructor_standings'] = constructor_standings
        except Exception as e:
            st.warning(f"Constructor standings data may have issues: {e}")
        
        data['_cache_time'] = file_mod_time  # Store for cache invalidation
        
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def clear_data_cache():
    """Clear the cached data"""
    load_data.clear()

def get_season_races(data, selected_season):
    """Get races for a specific season with circuit information"""
    season_races = data['races'][data['races']['year'] == selected_season].copy()
    season_races = season_races.merge(data['circuits'], on='circuitId', how='left')
    return season_races

def get_race_options(season_races):
    """Generate race options for selectbox"""
    race_options = []
    # Sort by round number to ensure correct order
    sorted_races = season_races.sort_values('round')
    for _, race in sorted_races.iterrows():
        race_options.append(f"Round {race['round']}: {race['name_x']}")
    return race_options