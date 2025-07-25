"""Race page display functions"""

import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from race_stats import display_race_stats
from qualifying import display_qualifying_data
from utils import race_has_sprint, time_to_seconds, format_time_mmssms, get_constructor_name, format_race_date, calculate_gap_to_leader

from team_colors import get_all_team_colors, get_team_color
from dataframe_styles import apply_dataframe_styles, create_starting_grid_layout
from card_styling import get_driver_team_color_for_race

def clean_display_value(value):
    """Clean display values by replacing \\N with -"""
    if pd.isna(value) or value == '\\N' or value == 'N' or str(value) == 'nan':
        return '-'
    return str(value)

def create_race_results_cards(grid_data, results_display, data, race_id):
    """Create individual cards for each race result, similar to starting grid"""
    
    # Create a single column layout for race results
    for i, result in enumerate(grid_data):
        # Get team color for this driver
        if race_id and i < len(results_display):
            driver_id = results_display.iloc[i]['driverId']
            team_color = get_driver_team_color_for_race(driver_id, race_id, data)
        else:
            team_color = '#808080'
        
        # Create individual result card
        with st.container():
            st.markdown(f"""
            <div style="border-left: 5px solid {team_color}; background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; display: flex; align-items: center;">
                <div style="color: black; width: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <strong style="font-size: 16px;">P{clean_display_value(result['POS.'])} - {clean_display_value(result['DRIVER'])}</strong><br>
                            <span style="color: #666; font-size: 13px;">{clean_display_value(result['TEAM'])}</span>
                        </div>
                        <div style="flex: 1; text-align: center;">
                            <span style="font-size: 15px; font-weight: 500;">{clean_display_value(result['TIME/RETIRED'])}</span>
                        </div>
                        <div style="flex: 0.5; text-align: center;">
                            <span style="font-size: 15px; font-weight: bold; color: #ff0000;">{clean_display_value(result['POINTS'])} pts</span>
                        </div>
                        <div style="flex: 0.5; text-align: center;">
                            <span style="font-size: 13px; color: #666;">{clean_display_value(result['LAPS'])} laps</span>
                        </div>
                        <div style="flex: 1; text-align: right;">
                            <span style="font-size: 13px; color: #666;">{clean_display_value(result['STATUS'])}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def create_sprint_results_cards(sprint_grid, sprint_display, data, race_id):
    """Create individual cards for each sprint result"""
    
    # Add header for sprint results
    st.markdown("""
    <div style="background: #e9ecef; padding: 10px; margin: 8px 0; border-radius: 5px; font-weight: bold; color: #495057;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">Position & Driver</div>
            <div style="flex: 1; text-align: center;">Time</div>
            <div style="flex: 0.5; text-align: center;">Points</div>
            <div style="flex: 0.5; text-align: center;">Laps</div>
            <div style="flex: 1; text-align: right;">Status</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a single column layout for sprint results
    for i, result in enumerate(sprint_grid):
        # Get team color for this driver
        if race_id and i < len(sprint_display):
            driver_id = sprint_display.iloc[i]['driverId']
            team_color = get_driver_team_color_for_race(driver_id, race_id, data)
        else:
            team_color = '#808080'
        
        # Create individual sprint result card
        with st.container():
            st.markdown(f"""
            <div style="border-left: 5px solid {team_color}; background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; display: flex; align-items: center;">
                <div style="color: black; width: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <strong style="font-size: 16px;">P{clean_display_value(result['POS.'])} - {clean_display_value(result['DRIVER'])}</strong><br>
                            <span style="color: #666; font-size: 13px;">{clean_display_value(result['TEAM'])}</span>
                        </div>
                        <div style="flex: 1; text-align: center;">
                            <span style="font-size: 15px; font-weight: 500;">{clean_display_value(result['TIME'])}</span>
                        </div>
                        <div style="flex: 0.5; text-align: center;">
                            <span style="font-size: 15px; font-weight: bold; color: #ff0000;">{clean_display_value(result['POINTS'])} pts</span>
                        </div>
                        <div style="flex: 0.5; text-align: center;">
                            <span style="font-size: 13px; color: #666;">{clean_display_value(result['LAPS'])} laps</span>
                        </div>
                        <div style="flex: 1; text-align: right;">
                            <span style="font-size: 13px; color: #666;">{clean_display_value(result['STATUS'])}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def create_driver_standings_cards(standings_grid, standings_display, data, race_id):
    """Create individual cards for each driver standing"""
    
    # Add header for driver standings
    st.markdown("""
    <div style="background: #e9ecef; padding: 10px; margin: 8px 0; border-radius: 5px; font-weight: bold; color: #495057;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">Position & Driver</div>
            <div style="flex: 0.6; text-align: center;">Points</div>
            <div style="flex: 0.5; text-align: center;">Wins</div>
            <div style="flex: 0.5; text-align: center;">Podiums</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a single column layout for driver standings
    for i, result in enumerate(standings_grid):
        # Get team color for this driver
        if race_id and i < len(standings_display):
            driver_id = standings_display.iloc[i]['driverId']
            team_color = get_driver_team_color_for_race(driver_id, race_id, data)
        else:
            team_color = '#808080'
        
        # Create individual driver standing card
        with st.container():
            st.markdown(f"""
            <div style="border-left: 5px solid {team_color}; background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; display: flex; align-items: center;">
                <div style="color: black; width: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <strong style="font-size: 16px;">P{clean_display_value(result['POS.'])} - {clean_display_value(result['DRIVER'])}</strong><br>
                            <span style="color: #666; font-size: 13px;">{clean_display_value(result['TEAM'])}</span>
                        </div>
                        <div style="flex: 0.6; text-align: center;">
                            <span style="font-size: 16px; font-weight: bold; color: #ff0000;">{clean_display_value(result['POINTS'])} pts</span>
                        </div>
                        <div style="flex: 0.5; text-align: center;">
                            <span style="font-size: 15px; font-weight: 500;">{clean_display_value(result['WINS'])}</span>
                        </div>
                        <div style="flex: 0.5; text-align: center;">
                            <span style="font-size: 15px; font-weight: 500;">{clean_display_value(result['PODIUMS'])}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def create_constructor_standings_cards(standings_grid, standings_display, data, race_id):
    """Create individual cards for each constructor standing"""
    
    # Add header for constructor standings
    st.markdown("""
    <div style="background: #e9ecef; padding: 10px; margin: 8px 0; border-radius: 5px; font-weight: bold; color: #495057;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">Position & Constructor</div>
            <div style="flex: 0.6; text-align: center;">Points</div>
            <div style="flex: 0.5; text-align: center;">Wins</div>
            <div style="flex: 0.5; text-align: center;">Podiums</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a single column layout for constructor standings
    for i, result in enumerate(standings_grid):
        # Get team color for this constructor
        if race_id and i < len(standings_display):
            constructor_ref = standings_display.iloc[i].get('constructorRef', 'default')
            from team_colors import get_team_color
            team_color = get_team_color(constructor_ref)
        else:
            team_color = '#808080'
        
        # Create individual constructor standing card
        with st.container():
            st.markdown(f"""
            <div style="border-left: 5px solid {team_color}; background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; display: flex; align-items: center;">
                <div style="color: black; width: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <strong style="font-size: 16px;">P{clean_display_value(result['POS.'])} - {clean_display_value(result['CONSTRUCTOR'])}</strong>
                        </div>
                        <div style="flex: 0.6; text-align: center;">
                            <span style="font-size: 16px; font-weight: bold; color: #ff0000;">{clean_display_value(result['POINTS'])} pts</span>
                        </div>
                        <div style="flex: 0.5; text-align: center;">
                            <span style="font-size: 15px; font-weight: 500;">{clean_display_value(result['WINS'])}</span>
                        </div>
                        <div style="flex: 0.5; text-align: center;">
                            <span style="font-size: 15px; font-weight: 500;">{clean_display_value(result['PODIUMS'])}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def lighten_color(hex_color, factor):
    """Lighten a hex color by a given factor (0.0 to 1.0)"""
    try:
        # Remove the # if present
        hex_color = hex_color.lstrip('#')
        
        # Convert hex to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Lighten the color
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
    except:
        return '#f8f9fa'  # Default light background

def display_race_page(race, data):
    """Display individual race page"""
    # Apply enhanced dataframe styles
    apply_dataframe_styles()
    
    display_race_header(race)
    st.divider()
    display_circuit_info(race)
    st.divider()
    
    # Display race stats cards (winner, pole position, fastest lap)
    race_results = data['results'][data['results']['raceId'] == race['raceId']]
    if not race_results.empty:
        display_race_stats(race_results, data)
        
        # Add a small space before the tabs
        st.write("")
        
        # Add a heading for the results view
        st.markdown("### Results View")
        
        # Check if this race has sprint data
        has_sprint = race_has_sprint(race['raceId'])
        
        # Create tabs with new order: Qualifying, Sprint Results, Starting Grid, Race Results, Driver Standings, Constructor Standings
        if has_sprint:
            tabs = st.tabs(["Qualifying", "Sprint Results", "Starting Grid", "Race Results", "Driver Standings", "Constructor Standings"])
            
            with tabs[0]:
                display_qualifying_data(race['raceId'], data)
            with tabs[1]:
                display_sprint_data(race['raceId'], data)
            with tabs[2]:
                display_starting_grid(race['raceId'], data)
            with tabs[3]:
                display_race_results_grid(race_results, data)
            with tabs[4]:
                display_driver_standings_after_race(race['raceId'], data)
            with tabs[5]:
                display_constructor_standings_after_race(race['raceId'], data)
        else:
            tabs = st.tabs(["Qualifying", "Starting Grid", "Race Results", "Driver Standings", "Constructor Standings"])
            
            with tabs[0]:
                display_qualifying_data(race['raceId'], data)
            with tabs[1]:
                display_starting_grid(race['raceId'], data)
            with tabs[2]:
                display_race_results_grid(race_results, data)
            with tabs[3]:
                display_driver_standings_after_race(race['raceId'], data)
            with tabs[4]:
                display_constructor_standings_after_race(race['raceId'], data)
    else:
        st.info("Race results not available for this race")

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
    return f"{minutes:02d}:{remaining_seconds:06.3f}"
        
# Qualifying function moved to qualifying.py module
        
    if not quali_results.empty:
            # Merge with driver and constructor data
            quali_display = quali_results.merge(data['drivers'], on='driverId', how='left')
            quali_display = quali_display.merge(data['constructors'], on='constructorId', how='left')
            
            # Prepare data for display
            quali_grid = []
            for _, row in quali_display.iterrows():
                constructor_name = get_constructor_name(row, data)
                
                # Format driver name with number (use number_x from results, fallback to number_y from drivers)
                driver_number = ""
                if 'number_x' in row.index and pd.notna(row['number_x']):
                    try:
                        driver_number = f"#{int(float(row['number_x']))}"
                    except (ValueError, TypeError):
                        if row['number_x'] != 'N' and row['number_x'] != '\\N':
                            driver_number = f"#{row['number_x']}"
                elif 'number_y' in row.index and pd.notna(row['number_y']):
                    try:
                        driver_number = f"#{int(float(row['number_y']))}"
                    except (ValueError, TypeError):
                        if row['number_y'] != 'N' and row['number_y'] != '\\N':
                            driver_number = f"#{row['number_y']}"
                
                driver_name = f"{row['forename']} {row['surname']}" if pd.notna(row['forename']) and pd.notna(row['surname']) else 'N/A'
                formatted_driver = f"{driver_number} {driver_name}".strip()
                
                quali_grid.append({
                    'POS.': int(row['position']) if pd.notna(row['position']) else '',
                    'DRIVER': formatted_driver,
                    'TEAM': constructor_name,
                    'Q1': row['q1'] if pd.notna(row['q1']) else '',
                    'Q2': row['q2'] if pd.notna(row['q2']) else '',
                    'Q3': row['q3'] if pd.notna(row['q3']) else ''
                })
            
            # Sort by position
            quali_grid = sorted(quali_grid, key=lambda x: x['POS.'] if x['POS.'] != '' else 999)
            
            # Display as DataFrame with larger text
            df = pd.DataFrame(quali_grid)
            
            # Custom CSS for larger text in dataframes
            st.markdown("""
            <style>
            .dataframe {
                font-size: 18px !important;
            }
            .dataframe th {
                font-size: 18px !important;
                font-weight: bold !important;
            }
            .dataframe td {
                font-size: 18px !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add interactive Plotly graph for comparing qualifying times
            st.write("")
            st.write("")
            st.markdown("### Compare Qualifying Times")
            
            # Create a dataframe for plotting
            plot_data = quali_display.copy()
            
            # Get list of drivers with Q1, Q2, Q3 data
            drivers_with_q1 = plot_data[plot_data['q1'].notna()][['driverId', 'forename', 'surname']].copy()
            drivers_with_q2 = plot_data[plot_data['q2'].notna()][['driverId', 'forename', 'surname']].copy()
            drivers_with_q3 = plot_data[plot_data['q3'].notna()][['driverId', 'forename', 'surname']].copy()
            
            # Create driver name list for each session
            drivers_q1 = [f"{row['forename']} {row['surname']}" for _, row in drivers_with_q1.iterrows()]
            drivers_q2 = [f"{row['forename']} {row['surname']}" for _, row in drivers_with_q2.iterrows()]
            drivers_q3 = [f"{row['forename']} {row['surname']}" for _, row in drivers_with_q3.iterrows()]
            
            # Create columns for the dropdowns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Default to first driver in Q3 if available, otherwise Q2, then Q1
                default_driver1 = drivers_q3[0] if drivers_q3 else (drivers_q2[0] if drivers_q2 else (drivers_q1[0] if drivers_q1 else None))
                driver1 = st.selectbox("Driver 1:", drivers_q1, index=drivers_q1.index(default_driver1) if default_driver1 in drivers_q1 else 0)
            
            with col2:
                # Default to second driver in Q3 if available, otherwise Q2, then Q1
                default_driver2 = drivers_q3[1] if len(drivers_q3) > 1 else (drivers_q2[1] if len(drivers_q2) > 1 else (drivers_q1[1] if len(drivers_q1) > 1 else None))
                driver2 = st.selectbox("Driver 2:", drivers_q1, index=drivers_q1.index(default_driver2) if default_driver2 in drivers_q1 else min(1, len(drivers_q1)-1))
            
            with col3:
                # Default to Q3
                session_options = ["Q1", "Q2", "Q3"]
                default_session = "Q3" if drivers_q3 else ("Q2" if drivers_q2 else "Q1")
                session = st.selectbox("Session:", session_options, index=session_options.index(default_session))
            
            # Use the global time conversion functions
            
            # Create a dataframe for the selected drivers and session
            driver1_data = plot_data[(plot_data['forename'] + ' ' + plot_data['surname']) == driver1].iloc[0]
            driver2_data = plot_data[(plot_data['forename'] + ' ' + plot_data['surname']) == driver2].iloc[0]
            
            # Get the times for the selected session
            session_col = session.lower()
            driver1_time = time_to_seconds(driver1_data[session_col])
            driver2_time = time_to_seconds(driver2_data[session_col])
            
            # Create a radar chart comparing the times
            if driver1_time is not None and driver2_time is not None:
                # Format times for display
                driver1_time_formatted = format_time_mmssms(driver1_time)
                driver2_time_formatted = format_time_mmssms(driver2_time)
                
                # Calculate the difference
                time_diff = abs(driver1_time - driver2_time)
                time_diff_formatted = format_time_mmssms(time_diff)
                faster_driver = driver1 if driver1_time < driver2_time else driver2
                
                # Create two comparison cards for qualifying times
                col1, col2 = st.columns(2)
                
                # Get driver numbers
                driver1_number = driver1_data.get('number', '')
                driver2_number = driver2_data.get('number', '')
                
                # Format driver numbers with # if available
                driver1_number_display = f"#{driver1_number}" if pd.notna(driver1_number) and driver1_number != '' else ""
                driver2_number_display = f"#{driver2_number}" if pd.notna(driver2_number) and driver2_number != '' else ""
                
                # Driver 1 card
                with col1:
                    st.markdown(
                        f"""
                        <div style="border:2px solid #ff0000; border-radius:10px; padding:20px; text-align:center;">
                            <h3 style="margin-top:0;">{driver1_number_display} {driver1}</h3>
                            <h2 style="font-size:28px; margin:15px 0;">{driver1_time_formatted}</h2>
                            <p style="margin-bottom:0; color:#888;">{session}</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                
                # Driver 2 card
                with col2:
                    st.markdown(
                        f"""
                        <div style="border:2px solid #ff0000; border-radius:10px; padding:20px; text-align:center;">
                            <h3 style="margin-top:0;">{driver2_number_display} {driver2}</h3>
                            <h2 style="font-size:28px; margin:15px 0;">{driver2_time_formatted}</h2>
                            <p style="margin-bottom:0; color:#888;">{session}</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                
                # Display the time difference below the cards
                st.markdown(
                    f"""
                    <div style="text-align:center; margin-top:15px;">
                        <p><strong>Time Difference:</strong> {time_diff_formatted} ({faster_driver} is faster by {time_diff:.3f} seconds)</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Create a line chart showing progression through Q1, Q2, Q3 if both drivers have data
                if pd.notna(driver1_data['q1']) and pd.notna(driver1_data['q2']) and pd.notna(driver1_data['q3']) and \
                   pd.notna(driver2_data['q1']) and pd.notna(driver2_data['q2']) and pd.notna(driver2_data['q3']):
                    
                    st.markdown("### Qualifying Progression")
                    
                    progression_data = pd.DataFrame({
                        'Session': ['Q1', 'Q2', 'Q3', 'Q1', 'Q2', 'Q3'],
                        'Driver': [driver1, driver1, driver1, driver2, driver2, driver2],
                        'Time (s)': [
                            time_to_seconds(driver1_data['q1']),
                            time_to_seconds(driver1_data['q2']),
                            time_to_seconds(driver1_data['q3']),
                            time_to_seconds(driver2_data['q1']),
                            time_to_seconds(driver2_data['q2']),
                            time_to_seconds(driver2_data['q3'])
                        ]
                    })
                    
                    fig = px.line(
                        progression_data, 
                        x='Session', 
                        y='Time (s)', 
                        color='Driver',
                        markers=True,
                        title=f"Qualifying Progression: {driver1} vs {driver2}"
                    )
                    
                    # Create formatted time labels for hover
                    time_labels = []
                    for time_val in progression_data['Time (s)']:
                        time_labels.append(format_time_mmssms(time_val))
                    
                    progression_data['Time_Formatted'] = time_labels
                    
                    fig.update_layout(
                        height=500,
                        yaxis=dict(
                            title="Lap Time",
                            # Use custom formatting for the y-axis ticks
                            tickmode='array',
                            tickvals=[progression_data['Time (s)'].min() - 0.5, progression_data['Time (s)'].max() + 0.5],
                            ticktext=[format_time_mmssms(progression_data['Time (s)'].min() - 0.5), 
                                     format_time_mmssms(progression_data['Time (s)'].max() + 0.5)]
                        ),
                        xaxis_title="Qualifying Session",
                        legend_title="Driver",
                        font=dict(size=14)
                    )
                    
                    # Add custom hover template to show time in MM:SS.ms format
                    fig.update_traces(
                        hovertemplate='<b>%{fullData.name}</b><br>Session: %{x}<br>Time: %{customdata}<extra></extra>',
                        customdata=[[label] for label in time_labels]
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"One or both drivers don't have {session} data available.")
# Qualifying function moved to qualifying.py module

def display_sprint_data(race_id, data):
    """Display sprint race data"""
    st.markdown("### Sprint Race Results")
    
    try:
        # Try to load sprint results data
        sprint_data = pd.read_csv('f1_data/sprint_results.csv')
        sprint_results = sprint_data[sprint_data['raceId'] == race_id]
        
        # Load status data for status descriptions
        status_data = pd.read_csv('f1_data/status.csv')
        
        if not sprint_results.empty:
            # Merge with driver and constructor data
            sprint_display = sprint_results.merge(data['drivers'], on='driverId', how='left')
            sprint_display = sprint_display.merge(data['constructors'], on='constructorId', how='left')
            sprint_display = sprint_display.merge(status_data, on='statusId', how='left')
            
            # Prepare data for display
            sprint_grid = []
            
            for _, row in sprint_display.iterrows():
                constructor_name = get_constructor_name(row, data)
                
                # Format driver name with number
                driver_number = ""
                if 'number' in row.index and pd.notna(row['number']):
                    try:
                        driver_number = f"#{int(float(row['number']))}"
                    except (ValueError, TypeError):
                        if str(row['number']) != 'N' and str(row['number']) != '\\N':
                            driver_number = f"#{row['number']}"
                
                driver_name = f"{row['forename']} {row['surname']}" if pd.notna(row['forename']) and pd.notna(row['surname']) else 'N/A'
                formatted_driver = f"{driver_number} {driver_name}".strip()
                
                # Get position safely
                position = ''
                if pd.notna(row['position']):
                    try:
                        position = int(float(row['position']))
                    except (ValueError, TypeError):
                        position = row['position']
                
                # Get points safely
                points = 0
                if pd.notna(row['points']):
                    try:
                        points = int(float(row['points']))
                    except (ValueError, TypeError):
                        points = float(row['points']) if isinstance(row['points'], (int, float)) else 0
                
                # Get laps safely
                laps = 0
                if pd.notna(row['laps']):
                    try:
                        laps = int(float(row['laps']))
                    except (ValueError, TypeError):
                        laps = row['laps']
                
                # Get status
                status = row['status'] if pd.notna(row.get('status')) else 'Unknown'
                
                sprint_grid.append({
                    'POS.': position,
                    'DRIVER': formatted_driver,
                    'TEAM': constructor_name,
                    'TIME': row['time'] if pd.notna(row['time']) else 'DNF',
                    'POINTS': points,
                    'LAPS': laps,
                    'STATUS': status
                })
            
            # Sort by position
            sprint_grid = sorted(sprint_grid, key=lambda x: (
                999 if x['POS.'] == '' or not isinstance(x['POS.'], int) else x['POS.']
            ))
            
            # Create sprint results cards
            create_sprint_results_cards(sprint_grid, sprint_display, data, race_id)
            

        else:
            st.info("Sprint race data not available for this race")
    except Exception as e:
        st.error(f"Error loading sprint data: {e}")
        st.info("Sprint race data not available for this race")

def display_starting_grid(race_id, data):
    """Display starting grid for the race with enhanced card layout"""
    st.markdown("### Starting Grid")
    
    try:
        # Get results data which contains grid positions
        race_results = data['results'][data['results']['raceId'] == race_id]
        
        if not race_results.empty:
            # Merge with driver and constructor data
            grid_display = race_results.merge(data['drivers'], on='driverId', how='left')
            grid_display = grid_display.merge(data['constructors'], on='constructorId', how='left')
            
            # Get team colors
            team_colors = get_all_team_colors()
            
            # Prepare data for display
            starting_grid = []
            for _, row in grid_display.iterrows():
                constructor_name = get_constructor_name(row, data)
                constructor_ref = row.get('constructorRef', 'default')
                
                # Format driver name with number (use number_x from results, fallback to number_y from drivers)
                driver_number = ""
                if 'number_x' in row.index and pd.notna(row['number_x']):
                    try:
                        driver_number = int(float(row['number_x']))
                    except (ValueError, TypeError):
                        driver_number = row['number_x'] if str(row['number_x']) not in ['N', '\\N'] else ""
                elif 'number_y' in row.index and pd.notna(row['number_y']):
                    try:
                        driver_number = int(float(row['number_y']))
                    except (ValueError, TypeError):
                        driver_number = row['number_y'] if str(row['number_y']) not in ['N', '\\N'] else ""
                
                driver_name = f"{row['forename']} {row['surname']}" if pd.notna(row['forename']) and pd.notna(row['surname']) else 'N/A'
                formatted_driver = f"#{driver_number} {driver_name}".strip() if driver_number else driver_name
                
                starting_grid.append({
                    'GRID POS.': int(row['grid']) if pd.notna(row['grid']) else '',
                    'DRIVER': formatted_driver,
                    'TEAM': constructor_name,
                    'team_ref': constructor_ref
                })
            
            # Display as enhanced card layout directly (no tabs)
            create_starting_grid_layout(starting_grid, team_colors)
        else:
            st.info("Starting grid data not available for this race")
    except Exception as e:
        st.error(f"Error loading starting grid data: {e}")
        st.info("Starting grid data not available for this race")

def display_race_data(race_id, data):
    """Display race results data"""
    race_results = data['results'][data['results']['raceId'] == race_id]
    
    if not race_results.empty:
        display_race_stats(race_results, data)
        display_race_results_grid(race_results, data)
    else:
        st.info("Race results not available for this race")

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

def display_race_header(race):
    """Display race header with title, circuit name, date and flag"""
    col1, col2, col3 = st.columns([2.8, 0.2, 1])
    
    with col1:
        st.markdown(f"## Round {race['round']}: {race['name_x']}")
        st.markdown(f"#### {race['name_y']}")
        st.write("")  # Add space between circuit name and date
        st.markdown(f"##### {format_race_date(race['date'])}")
    
    with col2:
        st.write("")  # Empty column for spacing
    
    with col3:
        st.write("")
        st.write("")
        display_country_flag(race)

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

def display_country_flag(race):
    """Display country flag using local images or fallback to URL"""
    # Get country name
    country = race['country'] if pd.notna(race['country']) else 'Unknown'
    
    # Try local flag image first, then fallback to URL
    local_flag = race.get('country_flag_local', '')
    original_flag = race.get('country_flag', '')
    
    flag_to_use = None
    
    # Check for local flag first
    if pd.notna(local_flag) and local_flag != '' and os.path.exists(local_flag):
        flag_to_use = local_flag
    elif pd.notna(original_flag) and original_flag != '':
        flag_to_use = original_flag
    
    if flag_to_use:
        try:
            # Display the flag image
            st.image(flag_to_use, width=220)
        except Exception as e:
            # Fallback to country name with emoji if image fails
            st.write(f"🏁 {country}")
    else:
        # Fallback for countries without flag images
        st.write(f"🏁 {country}")

def display_circuit_info(race):
    """Display circuit layout and details"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        display_circuit_image(race)
    
    with col2:
        display_circuit_details(race)

def display_circuit_image(race):
    """Display circuit layout image"""
    st.markdown("### Circuit Layout")
    
    # Try local image first, then fallback to URL
    local_image = race.get('circuit_image_local', '')
    original_image = race.get('circuit_image', '')
    
    image_to_use = None
    
    # Check for local image first
    if pd.notna(local_image) and local_image != '' and os.path.exists(local_image):
        image_to_use = local_image
    elif pd.notna(original_image) and original_image != '':
        image_to_use = original_image
    
    if image_to_use:
        try:
            st.image(image_to_use, width=600)  # Standard circuit image width
        except Exception as e:
            st.error("⚠️ Circuit image failed to load")
            st.info("This circuit image may be broken or unavailable")
            st.markdown("```\n🏁 Circuit layout not available\n```")
    else:
        st.info("Circuit image not available")

def display_circuit_details(race):
    """Display circuit details information with larger text"""
    st.markdown("### Circuit Details")
    
    # Display circuit length
    circuit_length = get_circuit_length(race)
    
    # Use HTML for larger text size
    st.markdown(f"""
    <div style="font-size: 18px; line-height: 1.6;">
        <p><strong>Location:</strong> {race['location']}</p>
        <p><strong>Country:</strong> {race['country']}</p>
        <p><strong>Length:</strong> {circuit_length}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display coordinates and altitude with larger text
    if pd.notna(race['lat']) and pd.notna(race['lng']):
        st.markdown(f"""
        <div style="font-size: 18px; line-height: 1.6;">
            <p><strong>Coordinates:</strong> {race['lat']:.4f}, {race['lng']:.4f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if pd.notna(race['alt']):
        st.markdown(f"""
        <div style="font-size: 18px; line-height: 1.6;">
            <p><strong>Altitude:</strong> {race['alt']}m</p>
        </div>
        """, unsafe_allow_html=True)

def get_circuit_length(race):
    """Get circuit length from race data"""
    try:
        if 'length' in race.index and pd.notna(race['length']):
            length_str = str(race['length'])
            if length_str not in ['Length not found', 'Error retrieving length', 'URL not available', '', 'nan']:
                return length_str
    except:
        pass
    return "Not available"

def display_race_results_grid(race_results, data):
    """Display race results with enhanced formatting and team information"""
    st.markdown("### Race Results")
    
    # Merge with driver and constructor data
    results_display = race_results.merge(data['drivers'], on='driverId', how='left')
    results_display = results_display.merge(data['constructors'], on='constructorId', how='left')
    
    # Load status data for status descriptions
    try:
        status_data = pd.read_csv('f1_data/status.csv')
        results_display = results_display.merge(status_data, on='statusId', how='left')
    except:
        pass
    
    # Prepare enhanced grid data with team information
    grid_data = []
    for _, row in results_display.iterrows():
        constructor_name = get_constructor_name(row, data)
        
        # Format driver name with number
        driver_number = ""
        if 'number_x' in row.index and pd.notna(row['number_x']):
            try:
                driver_number = f"#{int(float(row['number_x']))}"
            except (ValueError, TypeError):
                if str(row['number_x']) not in ['N', '\\N']:
                    driver_number = f"#{row['number_x']}"
        elif 'number_y' in row.index and pd.notna(row['number_y']):
            try:
                driver_number = f"#{int(float(row['number_y']))}"
            except (ValueError, TypeError):
                if str(row['number_y']) not in ['N', '\\N']:
                    driver_number = f"#{row['number_y']}"
        
        driver_name = f"{row['forename']} {row['surname']}" if pd.notna(row['forename']) and pd.notna(row['surname']) else 'N/A'
        formatted_driver = f"{driver_number} {driver_name}".strip()
        
        # Get position safely
        position = ''
        if pd.notna(row['position']):
            try:
                position = int(float(row['position']))
            except (ValueError, TypeError):
                position = row['position']
        
        # Get points safely
        points = 0
        if pd.notna(row['points']):
            try:
                points = int(float(row['points']))
            except (ValueError, TypeError):
                points = float(row['points']) if isinstance(row['points'], (int, float)) else 0
        
        # Get laps safely
        laps = 0
        if pd.notna(row['laps']):
            try:
                laps = int(float(row['laps']))
            except (ValueError, TypeError):
                laps = row['laps']
        
        # Get status
        status = row.get('status', 'Unknown') if pd.notna(row.get('status')) else 'Unknown'
        
        # Get time/gap
        time_result = row['time'] if pd.notna(row['time']) else 'DNF'
        
        grid_data.append({
            'POS.': position,
            'DRIVER': formatted_driver,
            'TEAM': constructor_name,
            'TIME/RETIRED': time_result,
            'POINTS': points,
            'LAPS': laps,
            'STATUS': status
        })
    
    # Sort by position
    grid_data = sorted(grid_data, key=lambda x: (
        999 if x['POS.'] == '' or not isinstance(x['POS.'], int) else x['POS.']
    ))
    
    # Create individual race result cards
    race_id = race_results['raceId'].iloc[0] if not race_results.empty else None
    
    # Add header for race results
    st.markdown("""
    <div style="background: #e9ecef; padding: 12px; margin: 10px 0; border-radius: 5px; font-weight: bold; color: #495057;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">Position & Driver</div>
            <div style="flex: 1; text-align: center;">Time</div>
            <div style="flex: 0.5; text-align: center;">Points</div>
            <div style="flex: 0.5; text-align: center;">Laps</div>
            <div style="flex: 1; text-align: right;">Status</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    create_race_results_cards(grid_data, results_display, data, race_id)
    
    # Add race analysis visualizations
    st.write("")
    st.markdown("### Race Analysis")
    
    # Check if we have lap times and pit stop data
    try:
        # Convert race_id to int to avoid comparison issues
        race_id_int = int(race_results['raceId'].iloc[0])
        
        lap_times = pd.read_csv('f1_data/lap_times.csv')
        race_lap_times = lap_times[lap_times['raceId'] == race_id_int]
        
        pit_stops = pd.read_csv('f1_data/pit_stops.csv')
        race_pit_stops = pit_stops[pit_stops['raceId'] == race_id_int]
        
        if not race_lap_times.empty:
            # Create tabs for different visualizations
            analysis_tabs = st.tabs(["Lap Time Comparison", "Position Progression", "Pit Stop Comparison", "Laps Led", "Pit Stop Summary"])
            
            with analysis_tabs[0]:
                # Lap Time Comparison - Select 2 drivers
                drivers_in_race = results_display[['driverId', 'forename', 'surname']].drop_duplicates()
                driver_options = [f"{row['forename']} {row['surname']}" for _, row in drivers_in_race.iterrows()]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_driver1 = st.selectbox("Select Driver 1:", driver_options, key="laptime_driver1")
                
                with col2:
                    selected_driver2 = st.selectbox("Select Driver 2:", driver_options, index=min(1, len(driver_options)-1), key="laptime_driver2")
                
                # Get driver IDs
                driver1_id = drivers_in_race[(drivers_in_race['forename'] + ' ' + drivers_in_race['surname']) == selected_driver1]['driverId'].iloc[0]
                driver2_id = drivers_in_race[(drivers_in_race['forename'] + ' ' + drivers_in_race['surname']) == selected_driver2]['driverId'].iloc[0]
                
                # Get lap times for selected drivers
                driver1_laps = race_lap_times[race_lap_times['driverId'] == driver1_id]
                driver2_laps = race_lap_times[race_lap_times['driverId'] == driver2_id]
                
                if not driver1_laps.empty and not driver2_laps.empty:
                    # Create a dataframe for plotting
                    lap_data = []
                    
                    for _, row in driver1_laps.iterrows():
                        lap_data.append({
                            'Driver': selected_driver1,
                            'Lap': row['lap'],
                            'Time (s)': row['milliseconds'] / 1000,
                            'Position': row['position']
                        })
                    
                    for _, row in driver2_laps.iterrows():
                        lap_data.append({
                            'Driver': selected_driver2,
                            'Lap': row['lap'],
                            'Time (s)': row['milliseconds'] / 1000,
                            'Position': row['position']
                        })
                    
                    lap_df = pd.DataFrame(lap_data)
                    
                    # Create lap time comparison chart
                    fig_laptime = px.line(
                        lap_df, 
                        x='Lap', 
                        y='Time (s)', 
                        color='Driver',
                        markers=True,
                        title=f"Lap Time Comparison: {selected_driver1} vs {selected_driver2}"
                    )
                    
                    # Apply team colors to the chart
                    try:
                        from graph_styling import apply_team_colors_to_existing_chart
                        fig_laptime = apply_team_colors_to_existing_chart(fig_laptime, lap_df, 'Driver', data, race_id_int)
                    except:
                        pass
                    
                    # Format y-axis to show minutes:seconds
                    fig_laptime.update_layout(
                        height=500,
                        yaxis=dict(
                            title="Lap Time",
                            tickmode='array',
                            tickvals=[lap_df['Time (s)'].min() - 0.5, lap_df['Time (s)'].max() + 0.5],
                            ticktext=[format_time_mmssms(lap_df['Time (s)'].min() - 0.5), 
                                     format_time_mmssms(lap_df['Time (s)'].max() + 0.5)]
                        ),
                        xaxis_title="Lap Number",
                        legend_title="Driver",
                        font=dict(size=16)
                    )
                    
                    # Add custom hover template to show time in MM:SS.ms format
                    for i, trace in enumerate(fig_laptime.data):
                        driver_data = lap_df[lap_df['Driver'] == trace.name]
                        formatted_times = [format_time_mmssms(t) for t in driver_data['Time (s)']]
                        fig_laptime.data[i].customdata = [[t] for t in formatted_times]
                        fig_laptime.data[i].hovertemplate = '<b>%{fullData.name}</b><br>Lap: %{x}<br>Time: %{customdata[0]}<extra></extra>'
                    
                    st.plotly_chart(fig_laptime, use_container_width=True)
                else:
                    st.info("Lap time data not available for selected drivers")
            
            with analysis_tabs[1]:
                # Position Progression - Select 2 drivers
                drivers_in_race = results_display[['driverId', 'forename', 'surname']].drop_duplicates()
                driver_options = [f"{row['forename']} {row['surname']}" for _, row in drivers_in_race.iterrows()]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    pos_driver1 = st.selectbox("Select Driver 1:", driver_options, key="position_driver1")
                
                with col2:
                    pos_driver2 = st.selectbox("Select Driver 2:", driver_options, index=min(1, len(driver_options)-1), key="position_driver2")
                
                # Get driver IDs
                pos_driver1_id = drivers_in_race[(drivers_in_race['forename'] + ' ' + drivers_in_race['surname']) == pos_driver1]['driverId'].iloc[0]
                pos_driver2_id = drivers_in_race[(drivers_in_race['forename'] + ' ' + drivers_in_race['surname']) == pos_driver2]['driverId'].iloc[0]
                
                # Get lap times for selected drivers
                pos_driver1_laps = race_lap_times[race_lap_times['driverId'] == pos_driver1_id]
                pos_driver2_laps = race_lap_times[race_lap_times['driverId'] == pos_driver2_id]
                
                if not pos_driver1_laps.empty and not pos_driver2_laps.empty:
                    # Create a dataframe for plotting
                    position_data = []
                    
                    for _, row in pos_driver1_laps.iterrows():
                        position_data.append({
                            'Driver': pos_driver1,
                            'Lap': row['lap'],
                            'Position': row['position']
                        })
                    
                    for _, row in pos_driver2_laps.iterrows():
                        position_data.append({
                            'Driver': pos_driver2,
                            'Lap': row['lap'],
                            'Position': row['position']
                        })
                    
                    position_df = pd.DataFrame(position_data)
                    
                    # Create position progression chart
                    fig_position = px.line(
                        position_df, 
                        x='Lap', 
                        y='Position', 
                        color='Driver',
                        markers=True,
                        title=f"Position Progression: {pos_driver1} vs {pos_driver2}"
                    )
                    
                    # Apply team colors to the chart
                    try:
                        from graph_styling import apply_team_colors_to_existing_chart
                        fig_position = apply_team_colors_to_existing_chart(fig_position, position_df, 'Driver', data, race_id_int)
                    except:
                        pass
                    
                    # Invert y-axis so that position 1 is at the top
                    fig_position.update_layout(
                        height=500,
                        yaxis=dict(
                            autorange="reversed",
                            title="Position",
                            dtick=1  # Show integer positions only
                        ),
                        xaxis_title="Lap Number",
                        legend_title="Driver",
                        font=dict(size=16)
                    )
                    
                    st.plotly_chart(fig_position, use_container_width=True)
                    
                    # Add position progression summary
                    st.write("")
                    st.markdown("**Position Progression Summary:**")
                    
                    # Get starting and ending positions
                    driver1_data = position_df[position_df['Driver'] == pos_driver1].sort_values('Lap')
                    driver2_data = position_df[position_df['Driver'] == pos_driver2].sort_values('Lap')
                    
                    if not driver1_data.empty and not driver2_data.empty:
                        # Starting positions
                        driver1_start = int(driver1_data.iloc[0]['Position'])
                        driver1_end = int(driver1_data.iloc[-1]['Position'])
                        driver2_start = int(driver2_data.iloc[0]['Position'])
                        driver2_end = int(driver2_data.iloc[-1]['Position'])
                        
                        # Position changes
                        driver1_change = driver1_start - driver1_end  # Positive = gained positions
                        driver2_change = driver2_start - driver2_end  # Positive = gained positions
                        
                        # Format position changes on same line
                        if driver1_change > 0:
                            st.write(f"• **{pos_driver1}**: Started P{driver1_start}, finished P{driver1_end}, gained {driver1_change} position(s)")
                        elif driver1_change < 0:
                            st.write(f"• **{pos_driver1}**: Started P{driver1_start}, finished P{driver1_end}, lost {abs(driver1_change)} position(s)")
                        else:
                            st.write(f"• **{pos_driver1}**: Started P{driver1_start}, finished P{driver1_end}, no net position change")
                        
                        if driver2_change > 0:
                            st.write(f"• **{pos_driver2}**: Started P{driver2_start}, finished P{driver2_end}, gained {driver2_change} position(s)")
                        elif driver2_change < 0:
                            st.write(f"• **{pos_driver2}**: Started P{driver2_start}, finished P{driver2_end}, lost {abs(driver2_change)} position(s)")
                        else:
                            st.write(f"• **{pos_driver2}**: Started P{driver2_start}, finished P{driver2_end}, no net position change")
                        
                        # Check for overtakes between the two drivers
                        overtakes = []
                        for i in range(len(driver1_data)):
                            lap = driver1_data.iloc[i]['Lap']
                            driver1_pos = driver1_data.iloc[i]['Position']
                            
                            # Find corresponding lap for driver2
                            driver2_lap_data = driver2_data[driver2_data['Lap'] == lap]
                            if not driver2_lap_data.empty:
                                driver2_pos = driver2_lap_data.iloc[0]['Position']
                                
                                # Check if positions crossed from previous lap
                                if i > 0:
                                    prev_lap = driver1_data.iloc[i-1]['Lap']
                                    prev_driver1_pos = driver1_data.iloc[i-1]['Position']
                                    prev_driver2_lap_data = driver2_data[driver2_data['Lap'] == prev_lap]
                                    
                                    if not prev_driver2_lap_data.empty:
                                        prev_driver2_pos = prev_driver2_lap_data.iloc[0]['Position']
                                        
                                        # Check if they swapped positions
                                        if ((prev_driver1_pos > prev_driver2_pos and driver1_pos < driver2_pos) or 
                                            (prev_driver1_pos < prev_driver2_pos and driver1_pos > driver2_pos)):
                                            if driver1_pos < driver2_pos:
                                                overtakes.append(f"Lap {lap}: {pos_driver1} overtook {pos_driver2}")
                                            else:
                                                overtakes.append(f"Lap {lap}: {pos_driver2} overtook {pos_driver1}")
                        
                        if overtakes:
                            st.write("• **Overtakes between drivers:**")
                            for overtake in overtakes:
                                st.write(f"  - {overtake}")
                        else:
                            st.write("• No direct overtakes between these drivers")
                else:
                    st.info("Position data not available for selected drivers")
            
            with analysis_tabs[2]:
                # Pit Stop Comparison between two drivers
                if not race_pit_stops.empty:
                    # Driver selection for pit stop comparison
                    drivers_in_race = results_display[['driverId', 'forename', 'surname']].drop_duplicates()
                    driver_options = [f"{row['forename']} {row['surname']}" for _, row in drivers_in_race.iterrows()]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        pit_driver1 = st.selectbox("Select Driver 1:", driver_options, key="pit_driver1")
                    
                    with col2:
                        pit_driver2 = st.selectbox("Select Driver 2:", driver_options, index=min(1, len(driver_options)-1), key="pit_driver2")
                    
                    # Get driver IDs
                    pit_driver1_id = drivers_in_race[(drivers_in_race['forename'] + ' ' + drivers_in_race['surname']) == pit_driver1]['driverId'].iloc[0]
                    pit_driver2_id = drivers_in_race[(drivers_in_race['forename'] + ' ' + drivers_in_race['surname']) == pit_driver2]['driverId'].iloc[0]
                    
                    # Get pit stop data for selected drivers
                    driver1_pitstops = race_pit_stops[race_pit_stops['driverId'] == pit_driver1_id].sort_values('stop')
                    driver2_pitstops = race_pit_stops[race_pit_stops['driverId'] == pit_driver2_id].sort_values('stop')
                    
                    # Display pit stop cards for both drivers
                    st.write("")
                    
                    # Driver 1 pit stops
                    if not driver1_pitstops.empty:
                        st.markdown(f"**{pit_driver1} Pit Stops:**")
                        cols1 = st.columns(min(len(driver1_pitstops), 4))
                        
                        for i, (_, pitstop) in enumerate(driver1_pitstops.iterrows()):
                            with cols1[i % 4]:
                                # Ensure duration is a float
                                try:
                                    duration = float(pitstop['duration'])
                                    duration_text = f"{duration:.3f}s"
                                except (ValueError, TypeError):
                                    duration_text = str(pitstop['duration'])
                                
                                st.markdown(
                                    f"""
                                    <div style="background-color:#f0f0f0; border:2px solid #ff0000; border-radius:8px; padding:15px; text-align:left; margin-bottom:8px; height: 150px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; overflow: hidden;">
                                        <h4 style="margin:0; color:#ff0000; font-weight:bold; font-size:16px; line-height: 1.2;">Pit Stop #{int(pitstop['stop'])}</h4>
                                        <h3 style="margin:0; color:#000000; font-weight:bold; font-size:18px; line-height: 1.2;">Lap {int(pitstop['lap'])}</h3>
                                        <p style="margin:0; color:#000; font-size:16px; font-weight: bold; line-height: 1.2;">{duration_text}</p>
                                    </div>
                                    """, 
                                    unsafe_allow_html=True
                                )
                    
                    st.write("")
                    
                    # Driver 2 pit stops
                    if not driver2_pitstops.empty:
                        st.markdown(f"**{pit_driver2} Pit Stops:**")
                        cols2 = st.columns(min(len(driver2_pitstops), 4))
                        
                        for i, (_, pitstop) in enumerate(driver2_pitstops.iterrows()):
                            with cols2[i % 4]:
                                # Ensure duration is a float
                                try:
                                    duration = float(pitstop['duration'])
                                    duration_text = f"{duration:.3f}s"
                                except (ValueError, TypeError):
                                    duration_text = str(pitstop['duration'])
                                
                                st.markdown(
                                    f"""
                                    <div style="background-color:#f0f0f0; border:2px solid #ff0000; border-radius:8px; padding:15px; text-align:left; margin-bottom:8px; height: 150px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; overflow: hidden;">
                                        <h4 style="margin:0; color:#ff0000; font-weight:bold; font-size:16px; line-height: 1.2;">Pit Stop #{int(pitstop['stop'])}</h4>
                                        <h3 style="margin:0; color:#000000; font-weight:bold; font-size:18px; line-height: 1.2;">Lap {int(pitstop['lap'])}</h3>
                                        <p style="margin:0; color:#000; font-size:16px; font-weight: bold; line-height: 1.2;">{duration_text}</p>
                                    </div>
                                    """, 
                                    unsafe_allow_html=True
                                )
                    
                    # Improved Summary Format
                    st.write("")
                    st.markdown("**Pit Stop Summary:**")
                    
                    if not driver1_pitstops.empty or not driver2_pitstops.empty:
                        # Compare each stop
                        max_stops = max(len(driver1_pitstops) if not driver1_pitstops.empty else 0, 
                                       len(driver2_pitstops) if not driver2_pitstops.empty else 0)
                        
                        for stop_num in range(1, max_stops + 1):
                            # Get data for this stop number
                            driver1_stop = driver1_pitstops[driver1_pitstops['stop'] == stop_num]
                            driver2_stop = driver2_pitstops[driver2_pitstops['stop'] == stop_num]
                            
                            if not driver1_stop.empty and not driver2_stop.empty:
                                # Both drivers have this stop
                                lap1 = int(driver1_stop.iloc[0]['lap'])
                                lap2 = int(driver2_stop.iloc[0]['lap'])
                                
                                try:
                                    duration1 = float(driver1_stop.iloc[0]['duration'])
                                    duration2 = float(driver2_stop.iloc[0]['duration'])
                                    
                                    lap_diff = lap1 - lap2
                                    duration_diff = duration1 - duration2
                                    
                                    if lap_diff == 0:
                                        # Same lap
                                        if abs(duration_diff) > 0.1:
                                            if duration_diff > 0:
                                                st.write(f"• Stop {stop_num}: Same lap, {pit_driver1} was {duration_diff:.3f}s slower")
                                            else:
                                                st.write(f"• Stop {stop_num}: Same lap, {pit_driver2} was {abs(duration_diff):.3f}s slower")
                                        else:
                                            st.write(f"• Stop {stop_num}: Same lap, similar duration")
                                    else:
                                        # Different laps
                                        if abs(duration_diff) > 0.1:
                                            if lap_diff > 0:
                                                if duration_diff > 0:
                                                    st.write(f"• Stop {stop_num}: {pit_driver1} pitted {lap_diff} lap(s) later, {pit_driver1} was {duration_diff:.3f}s slower")
                                                else:
                                                    st.write(f"• Stop {stop_num}: {pit_driver1} pitted {lap_diff} lap(s) later, {pit_driver2} was {abs(duration_diff):.3f}s slower")
                                            else:
                                                if duration_diff > 0:
                                                    st.write(f"• Stop {stop_num}: {pit_driver2} pitted {abs(lap_diff)} lap(s) later, {pit_driver1} was {duration_diff:.3f}s slower")
                                                else:
                                                    st.write(f"• Stop {stop_num}: {pit_driver2} pitted {abs(lap_diff)} lap(s) later, {pit_driver2} was {abs(duration_diff):.3f}s slower")
                                        else:
                                            if lap_diff > 0:
                                                st.write(f"• Stop {stop_num}: {pit_driver1} pitted {lap_diff} lap(s) later")
                                            else:
                                                st.write(f"• Stop {stop_num}: {pit_driver2} pitted {abs(lap_diff)} lap(s) later")
                                
                                except (ValueError, TypeError):
                                    # Handle non-numeric durations
                                    if lap_diff == 0:
                                        st.write(f"• Stop {stop_num}: Same lap")
                                    else:
                                        if lap_diff > 0:
                                            st.write(f"• Stop {stop_num}: {pit_driver1} pitted {lap_diff} lap(s) later")
                                        else:
                                            st.write(f"• Stop {stop_num}: {pit_driver2} pitted {abs(lap_diff)} lap(s) later")
                            
                            elif not driver1_stop.empty and driver2_stop.empty:
                                # Only driver1 has this stop
                                lap1 = int(driver1_stop.iloc[0]['lap'])
                                try:
                                    duration1 = float(driver1_stop.iloc[0]['duration'])
                                    st.write(f"• {pit_driver1} had an extra stop (Stop {stop_num}) at lap {lap1} for {duration1:.3f}s")
                                except (ValueError, TypeError):
                                    st.write(f"• {pit_driver1} had an extra stop (Stop {stop_num}) at lap {lap1}")
                            
                            elif driver1_stop.empty and not driver2_stop.empty:
                                # Only driver2 has this stop
                                lap2 = int(driver2_stop.iloc[0]['lap'])
                                try:
                                    duration2 = float(driver2_stop.iloc[0]['duration'])
                                    st.write(f"• {pit_driver2} had an extra stop (Stop {stop_num}) at lap {lap2} for {duration2:.3f}s")
                                except (ValueError, TypeError):
                                    st.write(f"• {pit_driver2} had an extra stop (Stop {stop_num}) at lap {lap2}")
                    
                    else:
                        st.write("• No pit stop data available for selected drivers")
                        
                else:
                    st.info("Pit stop data not available for this race")
            
            with analysis_tabs[3]:
                # Laps Led Analysis
                try:
                    # Get all lap times to analyze race leaders
                    all_laps = race_lap_times.copy()
                    
                    # Find laps where drivers were in position 1
                    leaders_data = all_laps[all_laps['position'] == 1].sort_values('lap')
                    
                    if not leaders_data.empty:
                        # Create race leadership progression (dot plot)
                        leaders_with_names = leaders_data.merge(data['drivers'], on='driverId', how='left')
                        leaders_with_names['driver_name'] = leaders_with_names.apply(
                            lambda x: f"{x['forename']} {x['surname']}", axis=1
                        )
                        
                        # Create dot plot showing race leader changes
                        fig_leadership = px.scatter(
                            leaders_with_names,
                            x='lap',
                            y='driver_name',
                            color='driver_name',
                            title="Race Leadership Progression",
                            labels={'lap': 'Lap Number', 'driver_name': 'Race Leader'}
                        )
                        
                        # Apply team colors to the chart
                        try:
                            from graph_styling import apply_team_colors_to_existing_chart
                            fig_leadership = apply_team_colors_to_existing_chart(fig_leadership, leaders_with_names, 'driver_name', data, race_id_int)
                        except:
                            pass
                        
                        fig_leadership.update_layout(
                            height=400,
                            xaxis_title="Lap Number",
                            yaxis_title="Race Leader",
                            font=dict(size=16),
                            showlegend=False
                        )
                        
                        st.plotly_chart(fig_leadership, use_container_width=True)
                        
                        # Group by driver and count laps led
                        laps_led = leaders_data.groupby('driverId').size().reset_index(name='laps_led')
                        
                        # Get driver names
                        laps_led = laps_led.merge(data['drivers'], on='driverId', how='left')
                        
                        # Format driver names
                        laps_led['driver_name'] = laps_led.apply(
                            lambda x: f"{x['forename']} {x['surname']}", axis=1
                        )
                        
                        # Create a bar chart of laps led
                        fig_leaders = px.bar(
                            laps_led,
                            x='driver_name',
                            y='laps_led',
                            title="Laps Led by Driver",
                            labels={'driver_name': 'Driver', 'laps_led': 'Laps Led'},
                            color='driver_name'
                        )
                        
                        # Apply team colors to the chart
                        try:
                            from graph_styling import apply_team_colors_to_existing_chart
                            fig_leaders = apply_team_colors_to_existing_chart(fig_leaders, laps_led, 'driver_name', data, race_id_int)
                        except:
                            pass
                        
                        fig_leaders.update_layout(
                            height=500,
                            xaxis_title="Driver",
                            yaxis_title="Number of Laps Led",
                            font=dict(size=16),
                            showlegend=False
                        )
                        
                        st.plotly_chart(fig_leaders, use_container_width=True)
                    else:
                        st.info("Race leader data not available")
                except Exception as e:
                    st.error(f"Error analyzing race leaders: {e}")
                    st.info("Laps led analysis not available")
            

            
            with analysis_tabs[4]:
                # Pit Stop Summary (overall race pit stop analysis)
                if not race_pit_stops.empty:
                    # Create a visualization of pit stop strategies
                    pit_stop_data = []
                    
                    for _, row in race_pit_stops.iterrows():
                        driver_info = drivers_in_race[drivers_in_race['driverId'] == row['driverId']]
                        if not driver_info.empty:
                            driver_name = f"{driver_info['forename'].iloc[0]} {driver_info['surname'].iloc[0]}"
                            # Ensure duration is a float
                            try:
                                duration = float(row['duration'])
                            except (ValueError, TypeError):
                                duration = 0.0
                                
                            pit_stop_data.append({
                                'Driver': driver_name,
                                'Stop': int(row['stop']) if pd.notna(row['stop']) else 0,
                                'Lap': int(row['lap']) if pd.notna(row['lap']) else 0,
                                'Duration (s)': duration
                            })
                    
                    if pit_stop_data:
                        pit_df = pd.DataFrame(pit_stop_data)
                        
                        # Create a bar chart of pit stop durations
                        fig2 = px.bar(
                            pit_df,
                            x='Driver',
                            y='Duration (s)',
                            color='Stop',
                            title="Pit Stop Durations",
                            labels={'Stop': 'Pit Stop Number'},
                            barmode='group'
                        )
                        
                        fig2.update_layout(
                            height=500,
                            xaxis_title="Driver",
                            yaxis_title="Duration (seconds)",
                            font=dict(size=14)
                        )
                        
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        st.info("No pit stop data available for visualization")
                else:
                    st.info("Pit stop data not available for this race")
        else:
            st.info("Lap time data not available for this race")
    except Exception as e:
        st.error(f"Error loading race analysis data: {e}")
        st.info("Race analysis not available")

def find_constructor_name_column(results_display):
    """Find the correct constructor name column"""
    for col in results_display.columns:
        if 'name' in col.lower() and col != 'name_x':
            return col
    return 'name' if 'name' in results_display.columns else 'constructorId'

def prepare_grid_data(results_display, constructor_name_col):
    """Prepare data for AG Grid display"""
    grid_data = []
    
    # Load status data for status descriptions
    try:
        status_data = pd.read_csv('f1_data/status.csv')
        results_display = results_display.merge(status_data, on='statusId', how='left')
    except:
        pass
    
    for _, row in results_display.iterrows():
        try:
            # Get proper constructor name using constructorId
            try:
                if 'name_y' in row.index and pd.notna(row['name_y']):
                    team_name = row['name_y']  # Constructor name from merge
                elif 'name' in row.index and pd.notna(row['name']) and row['name'] != row.get('forename', '') + ' ' + row.get('surname', ''):
                    team_name = row['name']  # Constructor name
                else:
                    team_name = 'N/A'
            except:
                team_name = 'N/A'
            
            # Format driver name with number (use number_x from results, fallback to number_y from drivers)
            driver_number = ""
            if 'number_x' in row.index and pd.notna(row['number_x']):
                try:
                    driver_number = f"#{int(float(row['number_x']))}"
                except (ValueError, TypeError):
                    if str(row['number_x']) != 'N' and str(row['number_x']) != '\\N':
                        driver_number = f"#{row['number_x']}"
            elif 'number_y' in row.index and pd.notna(row['number_y']):
                try:
                    driver_number = f"#{int(float(row['number_y']))}"
                except (ValueError, TypeError):
                    if str(row['number_y']) != 'N' and str(row['number_y']) != '\\N':
                        driver_number = f"#{row['number_y']}"
            
            driver_name = f"{row['forename']} {row['surname']}" if pd.notna(row['forename']) and pd.notna(row['surname']) else 'N/A'
            formatted_driver = f"{driver_number} {driver_name}".strip()
            
            # Get position safely
            position = ''
            if pd.notna(row['position']):
                try:
                    position = int(float(row['position']))
                except (ValueError, TypeError):
                    position = row['position']
            
            # Get points safely
            points = 0
            if pd.notna(row['points']):
                try:
                    points = int(float(row['points']))
                except (ValueError, TypeError):
                    points = float(row['points']) if isinstance(row['points'], (int, float)) else 0
            
            # Get laps safely
            laps = 0
            if pd.notna(row['laps']):
                try:
                    laps = int(float(row['laps']))
                except (ValueError, TypeError):
                    laps = row['laps']
            
            # Get status
            status = row['status'] if pd.notna(row.get('status')) else 'Unknown'
            
            # Add all rows, even if position is missing
            grid_data.append({
                'POS.': position,
                'DRIVER': formatted_driver,
                'TEAM': team_name,
                'TIME': row['time'] if pd.notna(row['time']) else 'DNF',
                'POINTS': points,
                'LAPS': laps,
                'STATUS': status
            })
        except Exception as e:
            # Log error but continue processing other rows
            st.warning(f"Error processing race result row: {e}")
            continue
    
    # Sort by position, handling non-numeric positions gracefully
    return sorted(grid_data, key=lambda x: (
        999 if x['POS.'] == '' or not isinstance(x['POS.'], int) else x['POS.']
    ))

def calculate_gap_to_leader(row, winner_milliseconds):
    """Calculate gap to race leader"""
    try:
        if row['position'] == 1:
            return ""
        elif winner_milliseconds is not None and pd.notna(row['milliseconds']):
            gap_ms = row['milliseconds'] - winner_milliseconds
            return f"+{gap_ms}ms" if gap_ms > 0 else ""
        else:
            return ""
    except:
        return ""

def configure_race_results_grid(df):
    """Configure AG Grid for race results"""
    gb = GridOptionsBuilder.from_dataframe(df)
    
    # Configure default column properties with larger text and left alignment
    gb.configure_default_column(
        resizable=True, 
        sortable=True, 
        filter=False, 
        editable=False,
        cellStyle={
            'font-size': '16px',
            'text-align': 'left',
            'padding-left': '10px'
        },
        headerClass='ag-header-cell-left'  # Left-align headers
    )
    
    # Define column widths based on content
    column_widths = {
        "POS.": 80,
        "DRIVER": 220,
        "TEAM": 180,
        "TIME": 120,
        "POINTS": 80,
        "LAPS": 80
    }
    
    # Configure each column with appropriate width
    for col in df.columns:
        if col in column_widths:
            if col in ["POS.", "DRIVER"]:
                gb.configure_column(col, width=column_widths[col], pinned='left')
            else:
                gb.configure_column(col, width=column_widths[col])
    
    # Calculate total width based on columns
    total_width = sum(column_widths.get(col, 120) for col in df.columns)
    
    # Set grid options with appropriate width
    gb.configure_grid_options(
        domLayout='normal',
        enableRangeSelection=True,
        rowSelection='single',
        width=total_width,
        headerHeight=40,  # Taller header
        rowHeight=40      # Taller rows
    )
    
    return gb.build()


def configure_sprint_grid(df):
    """Configure AG Grid for sprint results"""
    gb = GridOptionsBuilder.from_dataframe(df)
    
    # Configure default column properties with larger text and left alignment
    gb.configure_default_column(
        resizable=True, 
        sortable=True, 
        filter=False, 
        editable=False,
        cellStyle={
            'font-size': '16px',
            'text-align': 'left',
            'padding-left': '10px'
        },
        headerClass='ag-header-cell-left'  # Left-align headers
    )
    
    # Define column widths based on content
    column_widths = {
        "POS.": 80,
        "DRIVER": 220,
        "TEAM": 180,
        "TIME": 120,
        "POINTS": 80,
        "LAPS": 80,
        "STATUS": 120
    }
    
    # Configure each column with appropriate width
    for col in df.columns:
        if col in column_widths:
            if col in ["POS.", "DRIVER"]:
                gb.configure_column(col, width=column_widths[col], pinned='left')
            else:
                gb.configure_column(col, width=column_widths[col])
    
    # Calculate total width based on columns
    total_width = sum(column_widths.get(col, 120) for col in df.columns)
    
    # Set grid options with appropriate width
    gb.configure_grid_options(
        domLayout='normal',
        enableRangeSelection=True,
        rowSelection='single',
        width=total_width,
        headerHeight=40,  # Taller header
        rowHeight=40      # Taller rows
    )
    
    return gb.build()

def configure_starting_grid(df):
    """Configure AG Grid for starting grid"""
    gb = GridOptionsBuilder.from_dataframe(df)
    
    # Configure default column properties with larger text and left alignment
    gb.configure_default_column(
        resizable=True, 
        sortable=True, 
        filter=False, 
        editable=False,
        cellStyle={
            'font-size': '16px',
            'text-align': 'left',
            'padding-left': '10px'
        },
        headerClass='ag-header-cell-left'  # Left-align headers
    )
    
    # Define column widths based on content
    column_widths = {
        "GRID POS.": 100,
        "DRIVER": 220,
        "TEAM": 180
    }
    
    # Configure each column with appropriate width
    for col in df.columns:
        if col in column_widths:
            if col in ["GRID POS.", "DRIVER"]:
                gb.configure_column(col, width=column_widths[col], pinned='left')
            else:
                gb.configure_column(col, width=column_widths[col])
    
    # Calculate total width based on columns
    total_width = sum(column_widths.get(col, 120) for col in df.columns)
    
    # Set grid options with appropriate width
    gb.configure_grid_options(
        domLayout='normal',
        enableRangeSelection=True,
        rowSelection='single',
        width=total_width,
        headerHeight=40,  # Taller header
        rowHeight=40      # Taller rows
    )
    
    return gb.build()

def configure_standings_grid(df):
    """Configure AG Grid for championship standings"""
    gb = GridOptionsBuilder.from_dataframe(df)
    
    # Configure default column properties with larger text and left alignment
    gb.configure_default_column(
        resizable=True, 
        sortable=True, 
        filter=False, 
        editable=False,
        cellStyle={
            'font-size': '16px',
            'text-align': 'left',
            'padding-left': '10px'
        },
        headerClass='ag-header-cell-left'  # Left-align headers
    )
    
    # Define column widths based on content
    column_widths = {
        "POS.": 80,
        "DRIVER": 220,
        "CONSTRUCTOR": 220,
        "POINTS": 100,
        "WINS": 100,
        "PODIUMS": 100
    }
    
    # Configure each column with appropriate width
    for col in df.columns:
        if col in column_widths:
            if col in ["POS.", "DRIVER", "CONSTRUCTOR"] and (col == "DRIVER" and "DRIVER" in df.columns or col == "CONSTRUCTOR" and "CONSTRUCTOR" in df.columns or col == "POS."):
                gb.configure_column(col, width=column_widths[col], pinned='left')
            elif col in column_widths:
                gb.configure_column(col, width=column_widths[col])
    
    # Calculate total width based on columns
    total_width = sum(column_widths.get(col, 120) for col in df.columns)
    
    # Set grid options with appropriate width
    gb.configure_grid_options(
        domLayout='normal',
        enableRangeSelection=True,
        rowSelection='single',
        width=total_width,
        headerHeight=40,  # Taller header
        rowHeight=40      # Taller rows
    )
    
    return gb.build()

def display_driver_standings_after_race(race_id, data):
    """Display driver championship standings after this race"""
    st.markdown("### Driver Championship Standings")
    
    try:
        # Use pre-loaded driver standings if available, otherwise load from file
        if 'driver_standings' in data:
            standings_data = data['driver_standings']
        else:
            # Fallback to loading from file with special handling for NA values
            standings_data = pd.read_csv('f1_data/driver_standings.csv', na_values=['\\N', 'N'])
            # Convert problematic columns to appropriate types
            for col in ['position', 'points', 'wins']:
                if col in standings_data.columns:
                    standings_data[col] = pd.to_numeric(standings_data[col], errors='coerce')
        
        race_standings = standings_data[standings_data['raceId'] == race_id]
        
        # Check if we need to add sprint points
        has_sprint = race_has_sprint(race_id)
        if has_sprint:
            try:
                # Load sprint results
                sprint_data = pd.read_csv('f1_data/sprint_results.csv')
                sprint_results = sprint_data[sprint_data['raceId'] == race_id]
                
                if not sprint_results.empty:
                    # Create a mapping of driver points from sprint
                    sprint_points = {}
                    for _, row in sprint_results.iterrows():
                        if pd.notna(row['points']) and pd.notna(row['driverId']):
                            try:
                                driver_id = int(row['driverId'])
                                points = float(row['points'])
                                sprint_points[driver_id] = points
                            except:
                                pass
                    
                    # Add sprint points to driver standings
                    for i, row in race_standings.iterrows():
                        driver_id = int(row['driverId'])
                        if driver_id in sprint_points:
                            race_standings.at[i, 'points'] += sprint_points[driver_id]
            except Exception as e:
                st.warning(f"Could not add sprint points to driver standings: {e}")
        
        if not race_standings.empty:
            # Merge with driver and constructor data
            standings_display = race_standings.merge(data['drivers'], on='driverId', how='left')
            
            # Get constructor information for each driver at this race
            race_results = data['results'][data['results']['raceId'] == race_id]
            driver_constructors = race_results[['driverId', 'constructorId']].drop_duplicates()
            standings_display = standings_display.merge(driver_constructors, on='driverId', how='left')
            standings_display = standings_display.merge(data['constructors'], on='constructorId', how='left')
            
            # Calculate podium finishes for each driver
            try:
                # Get all race results up to this race to count podiums
                all_results = data['results'].copy()
                current_race = data['races'][data['races']['raceId'] == race_id]
                if not current_race.empty:
                    current_season = current_race['year'].iloc[0]
                    current_round = current_race['round'].iloc[0]
                    
                    # Get all races in current season up to this race
                    season_races = data['races'][(data['races']['year'] == current_season) & 
                                               (data['races']['round'] <= current_round)]
                    season_race_ids = season_races['raceId'].tolist()
                    
                    # Ensure position column is numeric and filter for podiums (2nd and 3rd only)
                    all_results['position'] = pd.to_numeric(all_results['position'], errors='coerce')
                    
                    # Count podiums (positions 2, 3 only - wins are counted separately) for each driver
                    podium_results = all_results[
                        (all_results['raceId'].isin(season_race_ids)) & 
                        (all_results['position'].isin([2, 3])) &
                        (all_results['position'].notna())
                    ]
                    
                    podium_counts = podium_results.groupby('driverId').size().to_dict()
                else:
                    podium_counts = {}
            except Exception as e:
                st.error(f"Could not calculate podium finishes: {e}")
                podium_counts = {}
            
            # Prepare data for display
            standings_grid = []
            for _, row in standings_display.iterrows():
                try:
                    # Format driver name with number (use number from drivers table)
                    driver_number = ""
                    if 'number' in row.index and pd.notna(row['number']):
                        # Convert to int safely
                        try:
                            driver_number = f"#{int(float(row['number']))}"
                        except (ValueError, TypeError):
                            # If conversion fails, try to use it as is
                            if str(row['number']) != 'N' and str(row['number']) != '\\N':
                                driver_number = f"#{row['number']}"
                    
                    driver_name = f"{row['forename']} {row['surname']}" if pd.notna(row['forename']) and pd.notna(row['surname']) else 'N/A'
                    formatted_driver = f"{driver_number} {driver_name}".strip()
                    
                    # Get constructor name
                    constructor_name = get_constructor_name(row, data)
                    
                    # Convert position to int safely
                    position = ''
                    if pd.notna(row['position']):
                        try:
                            position = int(float(row['position']))
                        except (ValueError, TypeError):
                            position = row['position']
                    
                    # Convert points to int safely
                    points = 0
                    if pd.notna(row['points']):
                        try:
                            points = int(float(row['points']))
                        except (ValueError, TypeError):
                            points = float(row['points']) if isinstance(row['points'], (int, float)) else 0
                    
                    # Convert wins to int safely
                    wins = 0
                    if pd.notna(row['wins']):
                        try:
                            wins = int(float(row['wins']))
                        except (ValueError, TypeError):
                            wins = float(row['wins']) if isinstance(row['wins'], (int, float)) else 0
                    
                    # Get podium count for this driver
                    driver_id = int(row['driverId']) if pd.notna(row['driverId']) else 0
                    podiums = podium_counts.get(driver_id, 0)
                    
                    standings_grid.append({
                        'POS.': position,
                        'DRIVER': formatted_driver,
                        'TEAM': constructor_name,
                        'POINTS': points,
                        'WINS': wins,
                        'PODIUMS': podiums
                    })
                except Exception as row_error:
                    # Skip problematic rows but log the error
                    st.warning(f"Skipped a driver due to data issue: {row_error}")
                    continue
            
            # Sort by position, handling non-numeric positions gracefully
            standings_grid = sorted(standings_grid, key=lambda x: (
                999 if x['POS.'] == '' or not isinstance(x['POS.'], int) else x['POS.']
            ))
            
            # Create driver standings cards
            create_driver_standings_cards(standings_grid, standings_display, data, race_id)
            
            # Add driver statistics with segmented controls
            st.write("")
            st.markdown("### Driver Championship Analysis")
            
            # Create tabs for different analysis views
            driver_analysis_tabs = st.tabs(["Points Progression", "Race Wins", "Podium Finishes", "Points Distribution"])
            
            with driver_analysis_tabs[0]:
                # Points Progression
                try:
                    # Get all driver standings for the season
                    current_race = data['races'][data['races']['raceId'] == race_id]
                    if not current_race.empty:
                        current_season = current_race['year'].iloc[0]
                        season_races = data['races'][data['races']['year'] == current_season]
                        season_race_ids = season_races[season_races['round'] <= current_race['round'].iloc[0]]['raceId'].tolist()
                        
                        if season_race_ids:
                            season_standings = data['driver_standings'][data['driver_standings']['raceId'].isin(season_race_ids)]
                            
                            if not season_standings.empty:
                                # Merge with races to get round numbers and driver names
                                season_standings = season_standings.merge(
                                    season_races[['raceId', 'round', 'name']], on='raceId', how='left')
                                season_standings = season_standings.merge(
                                    data['drivers'][['driverId', 'forename', 'surname']], on='driverId', how='left')
                                
                                # Create driver names
                                season_standings['driver_name'] = season_standings['forename'] + ' ' + season_standings['surname']
                                
                                # Create points progression chart
                                fig_progression = px.line(
                                    season_standings,
                                    x='round',
                                    y='points',
                                    color='driver_name',
                                    title="Driver Points Progression",
                                    labels={'round': 'Race Round', 'points': 'Points', 'driver_name': 'Driver'},
                                    markers=True
                                )
                                
                                # Apply team colors to the chart
                                try:
                                    from graph_styling import apply_team_colors_to_existing_chart
                                    fig_progression = apply_team_colors_to_existing_chart(fig_progression, season_standings, 'driver_name', data, race_id)
                                except:
                                    pass
                                
                                fig_progression.update_layout(
                                    height=500,
                                    xaxis_title="Race Round",
                                    yaxis_title="Points",
                                    font=dict(size=14)
                                )
                                
                                st.plotly_chart(fig_progression, use_container_width=True)
                            else:
                                st.info("Points progression data not available")
                        else:
                            st.info("No races found for current season")
                    else:
                        st.info("Race info not found for this race ID")
                except Exception as e:
                    st.error(f"Error generating points progression: {e}")
                    st.info("Points progression not available")
            
            with driver_analysis_tabs[1]:
                # Race Wins
                try:
                    if len(standings_grid) > 0:
                        points_data = pd.DataFrame(standings_grid)
                        wins_data = points_data[points_data['WINS'] > 0]
                        
                        if not wins_data.empty:
                            fig_wins = px.bar(
                                wins_data,
                                x='DRIVER',
                                y='WINS',
                                title="Race Wins by Driver",
                                color='DRIVER'
                            )
                            
                            # Apply team colors to the chart
                            try:
                                from graph_styling import get_driver_constructor_mapping, get_constructor_color_mapping
                                driver_constructor_mapping = get_driver_constructor_mapping(data, race_id)
                                constructor_color_mapping = get_constructor_color_mapping(data, race_id)
                                
                                # Extract driver names from formatted driver strings (remove numbers)
                                for trace in fig_wins.data:
                                    driver_display = trace.name  # e.g., "#4 Lando Norris"
                                    # Extract just the name part
                                    if ' ' in driver_display:
                                        driver_name = ' '.join(driver_display.split()[1:])  # Remove first part (number)
                                    else:
                                        driver_name = driver_display
                                    
                                    if driver_name in driver_constructor_mapping:
                                        constructor_name = driver_constructor_mapping[driver_name]
                                        if constructor_name in constructor_color_mapping:
                                            color = constructor_color_mapping[constructor_name]
                                            if hasattr(trace, 'marker'):
                                                trace.marker.color = color
                            except:
                                pass
                            
                            fig_wins.update_layout(
                                height=500,
                                xaxis_title="Driver",
                                yaxis_title="Number of Wins",
                                font=dict(size=14),
                                showlegend=False
                            )
                            
                            st.plotly_chart(fig_wins, use_container_width=True)
                        else:
                            st.info("No wins data available")
                    else:
                        st.info("No driver data available")
                except Exception as e:
                    st.error(f"Error generating wins chart: {e}")
            
            with driver_analysis_tabs[2]:
                # Podium Finishes
                try:
                    if len(standings_grid) > 0:
                        points_data = pd.DataFrame(standings_grid)
                        podium_data = points_data[points_data['PODIUMS'] > 0]
                        
                        if not podium_data.empty:
                            fig_podiums = px.bar(
                                podium_data,
                                x='DRIVER',
                                y='PODIUMS',
                                title="Podium Finishes by Driver",
                                color='DRIVER'
                            )
                            
                            # Apply team colors to the chart
                            try:
                                from graph_styling import get_driver_constructor_mapping, get_constructor_color_mapping
                                driver_constructor_mapping = get_driver_constructor_mapping(data, race_id)
                                constructor_color_mapping = get_constructor_color_mapping(data, race_id)
                                
                                # Extract driver names from formatted driver strings (remove numbers)
                                for trace in fig_podiums.data:
                                    driver_display = trace.name  # e.g., "#4 Lando Norris"
                                    # Extract just the name part
                                    if ' ' in driver_display:
                                        driver_name = ' '.join(driver_display.split()[1:])  # Remove first part (number)
                                    else:
                                        driver_name = driver_display
                                    
                                    if driver_name in driver_constructor_mapping:
                                        constructor_name = driver_constructor_mapping[driver_name]
                                        if constructor_name in constructor_color_mapping:
                                            color = constructor_color_mapping[constructor_name]
                                            if hasattr(trace, 'marker'):
                                                trace.marker.color = color
                            except:
                                pass
                            
                            fig_podiums.update_layout(
                                height=500,
                                xaxis_title="Driver",
                                yaxis_title="Number of Podiums",
                                font=dict(size=14),
                                showlegend=False
                            )
                            
                            st.plotly_chart(fig_podiums, use_container_width=True)
                        else:
                            st.info("No podium data available")
                    else:
                        st.info("No driver data available")
                except Exception as e:
                    st.error(f"Error generating podium chart: {e}")
            
            with driver_analysis_tabs[3]:
                # Points Distribution
                try:
                    if len(standings_grid) > 0:
                        points_data = pd.DataFrame(standings_grid)
                        points_data = points_data[points_data['POINTS'] > 0]
                        
                        if not points_data.empty:
                            fig_points = px.pie(
                                points_data,
                                values='POINTS',
                                names='DRIVER',
                                title="Points Distribution",
                                hole=0.4
                            )
                            
                            # Apply team colors to the pie chart
                            try:
                                from graph_styling import get_driver_constructor_mapping, get_constructor_color_mapping
                                driver_constructor_mapping = get_driver_constructor_mapping(data, race_id)
                                constructor_color_mapping = get_constructor_color_mapping(data, race_id)
                                
                                colors = []
                                for driver_display in points_data['DRIVER']:
                                    # Extract just the name part (remove number)
                                    if ' ' in driver_display:
                                        driver_name = ' '.join(driver_display.split()[1:])  # Remove first part (number)
                                    else:
                                        driver_name = driver_display
                                    
                                    if driver_name in driver_constructor_mapping:
                                        constructor_name = driver_constructor_mapping[driver_name]
                                        if constructor_name in constructor_color_mapping:
                                            colors.append(constructor_color_mapping[constructor_name])
                                        else:
                                            colors.append('#808080')
                                    else:
                                        colors.append('#808080')
                                
                                fig_points.update_traces(marker=dict(colors=colors))
                            except:
                                pass
                            
                            fig_points.update_layout(
                                height=500,
                                font=dict(size=14)
                            )
                            
                            st.plotly_chart(fig_points, use_container_width=True)
                        else:
                            st.info("No points data available")
                    else:
                        st.info("No driver data available")
                except Exception as e:
                    st.error(f"Error generating points distribution: {e}")
        else:
            st.info("Driver standings not available for this race")
    except Exception as e:
        st.error(f"Error loading driver standings: {e}")
        st.info("Driver standings not available for this race")

def display_constructor_standings_after_race(race_id, data):
    """Display constructor championship standings after this race"""
    st.markdown("### Constructor Championship Standings")
    
    try:
        if 'constructor_standings' in data:
            standings_data = data['constructor_standings']
        else:
            standings_data = pd.read_csv('f1_data/constructor_standings.csv', na_values=['\\N', 'N'])
            for col in ['position', 'points', 'wins']:
                if col in standings_data.columns:
                    standings_data[col] = pd.to_numeric(standings_data[col], errors='coerce')
        
        race_standings = standings_data[standings_data['raceId'] == race_id]
        
        has_sprint = race_has_sprint(race_id)
        if has_sprint:
            try:
                sprint_data = pd.read_csv('f1_data/sprint_results.csv')
                sprint_results = sprint_data[sprint_data['raceId'] == race_id]
                
                if not sprint_results.empty:
                    sprint_points = {}
                    for _, row in sprint_results.iterrows():
                        if pd.notna(row['points']) and pd.notna(row['constructorId']):
                            try:
                                constructor_id = int(row['constructorId'])
                                points = float(row['points'])
                                sprint_points[constructor_id] = sprint_points.get(constructor_id, 0) + points
                            except:
                                pass
                    
                    for i, row in race_standings.iterrows():
                        constructor_id = int(row['constructorId'])
                        if constructor_id in sprint_points:
                            race_standings.at[i, 'points'] += sprint_points[constructor_id]
            except Exception as e:
                st.warning(f"Could not add sprint points to constructor standings: {e}")
        
        if not race_standings.empty:
            standings_display = race_standings.merge(data['constructors'], on='constructorId', how='left')
            
            # Calculate podium finishes for each constructor
            try:
                # Get all race results up to this race to count podiums
                all_results = data['results'].copy()
                current_race = data['races'][data['races']['raceId'] == race_id]
                if not current_race.empty:
                    current_season = current_race['year'].iloc[0]
                    current_round = current_race['round'].iloc[0]
                    
                    # Get all races in current season up to this race
                    season_races = data['races'][(data['races']['year'] == current_season) & 
                                               (data['races']['round'] <= current_round)]
                    season_race_ids = season_races['raceId'].tolist()
                    
                    # Ensure position column is numeric and filter for podiums (2nd and 3rd only)
                    all_results['position'] = pd.to_numeric(all_results['position'], errors='coerce')
                    
                    # Count podiums (positions 2, 3 only - wins are counted separately) for each constructor
                    podium_results = all_results[
                        (all_results['raceId'].isin(season_race_ids)) & 
                        (all_results['position'].isin([2, 3])) &
                        (all_results['position'].notna())
                    ]
                    podium_counts = podium_results.groupby('constructorId').size().to_dict()
                else:
                    podium_counts = {}
            except Exception as e:
                st.warning(f"Could not calculate constructor podium finishes: {e}")
                podium_counts = {}
            
            standings_grid = []

            for _, row in standings_display.iterrows():
                try:
                    position = ''
                    if pd.notna(row['position']):
                        try:
                            position = int(float(row['position']))
                        except:
                            position = row['position']
                    
                    points = 0
                    if pd.notna(row['points']):
                        try:
                            points = int(float(row['points']))
                        except:
                            points = float(row['points']) if isinstance(row['points'], (int, float)) else 0
                    
                    wins = 0
                    if pd.notna(row['wins']):
                        try:
                            wins = int(float(row['wins']))
                        except:
                            wins = float(row['wins']) if isinstance(row['wins'], (int, float)) else 0
                    
                    # Get podium count for this constructor
                    constructor_id = int(row['constructorId']) if pd.notna(row['constructorId']) else 0
                    podiums = podium_counts.get(constructor_id, 0)
                    
                    standings_grid.append({
                        'POS.': position,
                        'CONSTRUCTOR': row['name'] if pd.notna(row['name']) else 'N/A',
                        'POINTS': points,
                        'WINS': wins,
                        'PODIUMS': podiums
                    })
                except Exception as row_error:
                    st.warning(f"Skipped a constructor due to data issue: {row_error}")
                    continue
            
            standings_grid = sorted(standings_grid, key=lambda x: (
                999 if x['POS.'] == '' or not isinstance(x['POS.'], int) else x['POS.']
            ))
            
            # Create constructor standings cards
            create_constructor_standings_cards(standings_grid, standings_display, data, race_id)
            
            st.write("")
            st.markdown("### Constructor Championship Analysis")
            constructor_analysis_tabs = st.tabs(["Points Progression", "Race Wins", "Podium Finishes", "Points Distribution"])
            
            with constructor_analysis_tabs[0]:
                try:
                    races = data['races']
                    season_standings = standings_data.copy()
                    current_race = races[races['raceId'] == race_id]
                    
                    if not current_race.empty:
                        current_season = current_race['year'].iloc[0]
                        season_races = races[races['year'] == current_season]
                        season_race_ids = season_races[season_races['round'] <= current_race['round'].iloc[0]]['raceId'].tolist()
                        
                        if season_race_ids:
                            season_standings = season_standings[season_standings['raceId'].isin(season_race_ids)]
                            
                            if not season_standings.empty:
                                season_standings = season_standings.merge(
                                    races[['raceId', 'round', 'name']], on='raceId', how='left')
                                season_standings = season_standings.merge(
                                    data['constructors'][['constructorId', 'name']], on='constructorId', how='left', suffixes=('', '_constructor'))
                                
                                fig_progression = px.line(
                                    season_standings,
                                    x='round',
                                    y='points',
                                    color='name_constructor',
                                    title="Constructor Points Progression",
                                    labels={'round': 'Race Round', 'points': 'Points', 'name_constructor': 'Constructor'},
                                    markers=True
                                )
                                
                                # Apply team colors to the chart
                                try:
                                    from graph_styling import get_constructor_color_mapping
                                    constructor_colors = get_constructor_color_mapping(data, race_id)
                                    for trace in fig_progression.data:
                                        constructor_name = trace.name
                                        if constructor_name in constructor_colors:
                                            color = constructor_colors[constructor_name]
                                            if hasattr(trace, 'marker'):
                                                trace.marker.color = color
                                            if hasattr(trace, 'line'):
                                                trace.line.color = color
                                except:
                                    pass
                                
                                fig_progression.update_layout(
                                    height=500,
                                    xaxis_title="Race Round",
                                    yaxis_title="Points",
                                    font=dict(size=14)
                                )
                                
                                st.plotly_chart(fig_progression, use_container_width=True)
                            else:
                                st.info("Points progression not available")
                        else:
                            st.info("No races found for current season")
                    else:
                        st.info("Race info not found for this race ID")
                except Exception as e:
                    st.error(f"Error generating points progression: {e}")
                    st.info("Points progression not available")
            
            with constructor_analysis_tabs[1]:
                try:
                    if len(standings_grid) > 0:
                        points_data = pd.DataFrame(standings_grid)
                        wins_data = points_data[points_data['WINS'] > 0]
                        
                        if not wins_data.empty:
                            fig_wins = px.bar(
                                wins_data,
                                x='CONSTRUCTOR',
                                y='WINS',
                                title="Race Wins by Constructor",
                                color='CONSTRUCTOR'
                            )
                            
                            # Apply team colors to the chart
                            try:
                                from graph_styling import get_constructor_color_mapping
                                constructor_colors = get_constructor_color_mapping(data, race_id)
                                for trace in fig_wins.data:
                                    constructor_name = trace.name
                                    if constructor_name in constructor_colors:
                                        color = constructor_colors[constructor_name]
                                        if hasattr(trace, 'marker'):
                                            trace.marker.color = color
                            except:
                                pass
                            
                            fig_wins.update_layout(
                                height=500,
                                xaxis_title="Constructor",
                                yaxis_title="Number of Wins",
                                font=dict(size=14),
                                showlegend=False
                            )
                            st.plotly_chart(fig_wins, use_container_width=True)
                        else:
                            st.info("No wins data available")
                    else:
                        st.info("No constructor data available")
                except Exception as e:
                    st.error(f"Error generating wins chart: {e}")
            
            with constructor_analysis_tabs[2]:
                # Podium Finishes
                try:
                    if len(standings_grid) > 0:
                        points_data = pd.DataFrame(standings_grid)
                        podium_data = points_data[points_data['PODIUMS'] > 0]
                        
                        if not podium_data.empty:
                            fig_podiums = px.bar(
                                podium_data,
                                x='CONSTRUCTOR',
                                y='PODIUMS',
                                title="Podium Finishes by Constructor",
                                color='CONSTRUCTOR'
                            )
                            
                            # Apply team colors to the chart
                            try:
                                from graph_styling import get_constructor_color_mapping
                                constructor_colors = get_constructor_color_mapping(data, race_id)
                                for trace in fig_podiums.data:
                                    constructor_name = trace.name
                                    if constructor_name in constructor_colors:
                                        color = constructor_colors[constructor_name]
                                        if hasattr(trace, 'marker'):
                                            trace.marker.color = color
                            except:
                                pass
                            
                            fig_podiums.update_layout(
                                height=500,
                                xaxis_title="Constructor",
                                yaxis_title="Number of Podiums",
                                font=dict(size=14),
                                showlegend=False
                            )
                            
                            st.plotly_chart(fig_podiums, use_container_width=True)
                        else:
                            st.info("No podium data available")
                    else:
                        st.info("No constructor data available")
                except Exception as e:
                    st.error(f"Error generating podium chart: {e}")
            
            with constructor_analysis_tabs[3]:
                # Points Distribution
                try:
                    if len(standings_grid) > 0:
                        points_data = pd.DataFrame(standings_grid)
                        points_data = points_data[points_data['POINTS'] > 0]
                        
                        if not points_data.empty:
                            fig_points = px.pie(
                                points_data,
                                values='POINTS',
                                names='CONSTRUCTOR',
                                title="Points Distribution",
                                hole=0.4
                            )
                            
                            # Apply team colors to the pie chart
                            try:
                                from graph_styling import get_constructor_color_mapping
                                constructor_colors = get_constructor_color_mapping(data, race_id)
                                
                                colors = []
                                for constructor_name in points_data['CONSTRUCTOR']:
                                    if constructor_name in constructor_colors:
                                        colors.append(constructor_colors[constructor_name])
                                    else:
                                        colors.append('#808080')
                                
                                fig_points.update_traces(marker=dict(colors=colors))
                            except:
                                pass
                            
                            fig_points.update_layout(height=500, font=dict(size=14))
                            st.plotly_chart(fig_points, use_container_width=True)
                        else:
                            st.info("No points data available")
                    else:
                        st.info("No constructor data available")
                except Exception as e:
                    st.error(f"Error generating points distribution: {e}")
        else:
            st.info("Constructor standings not available for this race")
    except Exception as e:
        st.error(f"Error loading constructor standings: {e}")
        st.info("Constructor standings not available for this race")
