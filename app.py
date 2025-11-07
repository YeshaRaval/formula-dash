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
        
        # Find the most recent season with race results
        default_season_index = 0
        for idx, season in enumerate(seasons):
            season_race_ids = data['races'][data['races']['year'] == season]['raceId'].values
            if len(data['results'][data['results']['raceId'].isin(season_race_ids)]) > 0:
                default_season_index = idx
                break
        
        selected_season = st.selectbox("📅 Select Season", seasons, index=default_season_index, key="season_select")
    
    # Get races for selected season
    season_races = get_season_races(data, selected_season)
    race_options = get_race_options(season_races)
    
    if race_options:
        # Store season races in session state for navigation
        st.session_state['season_races'] = season_races
        st.session_state['max_round'] = season_races['round'].max()
        st.session_state['current_season'] = selected_season
        
        with col2:
            # Determine default race - find the most recent race with results
            default_index = 0
            
            # Check if season changed to reset race selection
            previous_season = st.session_state.get('previous_season', None)
            season_changed = previous_season is not None and previous_season != selected_season
            st.session_state['previous_season'] = selected_season
            
            # Find the most recent race with results for this season
            if season_changed or 'navigate_to_round' not in st.session_state:
                latest_race_with_results = None
                for _, race in season_races.sort_values('round', ascending=False).iterrows():
                    race_results = data['results'][data['results']['raceId'] == race['raceId']]
                    if len(race_results) > 0:
                        latest_race_with_results = race['round']
                        break
                
                if latest_race_with_results:
                    for i, option in enumerate(race_options):
                        round_num = int(option.split(":")[0].replace("Round ", ""))
                        if round_num == latest_race_with_results:
                            default_index = i
                            break
            
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