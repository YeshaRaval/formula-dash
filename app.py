"""F1 Statistics Dashboard - Main Application"""

import streamlit as st
from config import setup_page_config, apply_custom_css
from data_loader import load_data, get_season_races, get_race_options
from race_display import display_race_page

setup_page_config()
apply_custom_css()

def main():
    """Main application function"""
    # Load data
    data = load_data()
    if data is None:
        st.stop()
    
    # Create top navigation for race selection
    create_top_navigation(data)

def create_top_navigation(data):
    """Create top navigation with season and race selection using selectboxes"""
    
    # Title
    st.markdown("# 🏎️ F1 Statistics Dashboard")
    
    # Create two columns for season and race selection
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Season filter
        seasons = sorted(data['races']['year'].unique(), reverse=True)
        # Find 2025 season index if it exists
        try:
            season_2025_index = seasons.index(2025) if 2025 in seasons else 0
        except:
            season_2025_index = 0
        
        selected_season = st.selectbox("📅 Select Season", seasons, index=season_2025_index, key="season_select")
    
    # Get races for selected season
    season_races = get_season_races(data, selected_season)
    race_options = get_race_options(season_races)
    
    if race_options:
        # Store season races in session state for navigation
        st.session_state['season_races'] = season_races
        st.session_state['max_round'] = season_races['round'].max()
        st.session_state['current_season'] = selected_season
        
        with col2:
            # Determine default race based on season
            default_index = 0
            
            # Check if season changed to reset race selection
            previous_season = st.session_state.get('previous_season', None)
            season_changed = previous_season is not None and previous_season != selected_season
            st.session_state['previous_season'] = selected_season
            
            if selected_season == 2025:
                # For 2025, default to British Grand Prix if available
                for i, option in enumerate(race_options):
                    if "British" in option:
                        default_index = i
                        break
            else:
                # For other years, default to Round 1 (first race)
                default_index = 0
            
            # Check if we need to navigate to a specific round (but not if season just changed)
            navigate_to_round = st.session_state.get('navigate_to_round', None)
            if navigate_to_round is not None and not season_changed:
                for i, option in enumerate(race_options):
                    round_num = int(option.split(":")[0].replace("Round ", ""))
                    if round_num == navigate_to_round:
                        default_index = i
                        st.session_state['navigate_to_round'] = None
                        break
            
            # Race selection
            selected_race_display = st.selectbox("🏁 Select Race", race_options, index=default_index, key="race_select")
            selected_round = int(selected_race_display.split(":")[0].replace("Round ", ""))
            selected_race = season_races[season_races['round'] == selected_round].iloc[0]
        
        # Add a separator
        st.markdown("---")
        
        # Display selected race page
        display_race_page(selected_race, data)
    else:
        st.error("No races found for selected season")

if __name__ == "__main__":
    main()