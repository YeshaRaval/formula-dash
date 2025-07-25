"""Qualifying data display functions"""

import streamlit as st
import pandas as pd
import plotly.express as px

from utils import time_to_seconds, format_time_mmssms, get_constructor_name

from graph_styling import apply_team_colors_to_existing_chart, get_driver_constructor_mapping
from card_styling import get_driver_team_color_for_race

def clean_display_value(value):
    """Clean display values by replacing \\N with -"""
    if pd.isna(value) or value == '\\N' or value == 'N' or str(value) == 'nan':
        return '-'
    return str(value)

def create_qualifying_cards(quali_grid, quali_display, data, race_id):
    """Create individual cards for each qualifying result"""
    
    # Add header for qualifying results
    st.markdown("""
    <div style="background: #e9ecef; padding: 10px; margin: 8px 0; border-radius: 5px; font-weight: bold; color: #495057;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">Position & Driver</div>
            <div style="flex: 0.8; text-align: center;">Q1</div>
            <div style="flex: 0.8; text-align: center;">Q2</div>
            <div style="flex: 0.8; text-align: center;">Q3</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a single column layout for qualifying results
    for i, result in enumerate(quali_grid):
        # Get team color for this driver
        if race_id and i < len(quali_display):
            driver_id = quali_display.iloc[i]['driverId']
            team_color = get_driver_team_color_for_race(driver_id, race_id, data)
        else:
            team_color = '#808080'
        
        # Create individual qualifying card
        with st.container():
            st.markdown(f"""
            <div style="border-left: 5px solid {team_color}; background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; display: flex; align-items: center;">
                <div style="color: black; width: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <strong style="font-size: 16px;">P{clean_display_value(result['POS.'])} - {clean_display_value(result['DRIVER'])}</strong><br>
                            <span style="color: #666; font-size: 13px;">{clean_display_value(result['TEAM'])}</span>
                        </div>
                        <div style="flex: 0.8; text-align: center;">
                            <span style="font-size: 15px; font-weight: 500;">{clean_display_value(result['Q1']) if result['Q1'] else '-'}</span>
                        </div>
                        <div style="flex: 0.8; text-align: center;">
                            <span style="font-size: 15px; font-weight: 500;">{clean_display_value(result['Q2']) if result['Q2'] else '-'}</span>
                        </div>
                        <div style="flex: 0.8; text-align: center;">
                            <span style="font-size: 15px; font-weight: 500; color: #ff0000;">{clean_display_value(result['Q3']) if result['Q3'] else '-'}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def display_qualifying_data(race_id, data):
    """Display qualifying session data"""
    st.markdown("### Qualifying Results")
    
    try:
        # Try to load qualifying data
        qualifying_data = pd.read_csv('f1_data/qualifying.csv')
        quali_results = qualifying_data[qualifying_data['raceId'] == race_id]
        
        if not quali_results.empty:
            # Merge with driver and constructor data
            quali_display = quali_results.merge(data['drivers'], on='driverId', how='left')
            quali_display = quali_display.merge(data['constructors'], on='constructorId', how='left')
            
            # Prepare data for display
            quali_grid = []
            for _, row in quali_display.iterrows():
                constructor_name = get_constructor_name(row, data)
                
                # Format driver name with number
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
            
            # Create qualifying cards
            create_qualifying_cards(quali_grid, quali_display, data, race_id)
            
            # Add qualifying analysis section
            st.write("")
            st.markdown("### Qualifying Analysis")
            
            # Create tabs for different analysis views
            analysis_tabs = st.tabs(["Session Best Times", "Compare Lap Times", "Qualifying Progression"])
            
            with analysis_tabs[0]:
                display_session_best_times(quali_display, data, race_id)
            
            with analysis_tabs[1]:
                display_qualifying_comparison(quali_display, data, race_id)
            
            with analysis_tabs[2]:
                display_qualifying_progression_all_drivers(quali_display, data, race_id)
                
        else:
            st.info("Qualifying data not available for this race")
    except Exception as e:
        st.error(f"Error loading qualifying data: {e}")
        st.info("Qualifying data not available for this race")

def display_session_best_times(quali_display, data, race_id=None):
    """Display session best times in cards"""
    
    # Find best times for each session
    sessions = ['Q1', 'Q2', 'Q3']
    session_colors = ['#ff0000', '#ff0000', '#ff0000']  # All bright red
    
    # Create three columns for the cards
    cols = st.columns(3)
    
    for i, session in enumerate(sessions):
        session_col = session.lower()
        session_data = quali_display[quali_display[session_col].notna()].copy()
        
        if not session_data.empty:
            # Convert times to seconds for comparison
            session_data['time_seconds'] = session_data[session_col].apply(time_to_seconds)
            session_data = session_data[session_data['time_seconds'].notna()]
            
            if not session_data.empty:
                # Find fastest time
                fastest_row = session_data.loc[session_data['time_seconds'].idxmin()]
                
                # Format data
                driver_surname = fastest_row['surname']
                driver_number = ""
                if 'number_x' in fastest_row.index and pd.notna(fastest_row['number_x']):
                    try:
                        driver_number = f"#{int(float(fastest_row['number_x']))}"
                    except (ValueError, TypeError):
                        if fastest_row['number_x'] != 'N' and fastest_row['number_x'] != '\\N':
                            driver_number = f"#{fastest_row['number_x']}"
                elif 'number_y' in fastest_row.index and pd.notna(fastest_row['number_y']):
                    try:
                        driver_number = f"#{int(float(fastest_row['number_y']))}"
                    except (ValueError, TypeError):
                        if fastest_row['number_y'] != 'N' and fastest_row['number_y'] != '\\N':
                            driver_number = f"#{fastest_row['number_y']}"
                
                time_formatted = format_time_mmssms(fastest_row['time_seconds'])
                
                # Get team color for the fastest driver
                driver_id = fastest_row['driverId']
                team_color = get_driver_team_color_for_race(driver_id, race_id, data)
                
                with cols[i]:
                    st.markdown(
                        f"""
                        <div style="background-color:#f8f9fa; border-left: 5px solid {team_color}; border-radius:10px; padding:12px; text-align:left; width: 80%; margin: 0 auto;">
                            <h4 style="margin-top:0; margin-bottom:8px; color:#FF0000; font-weight:bold; font-size:16px;">Best {session} Time</h4>
                            <h3 style="margin:5px 0; color:#000000; font-weight:bold; font-size:18px;">{driver_number} {driver_surname}</h3>
                            <p style="margin-bottom:0; color:#666; font-size:14px;">{time_formatted}</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
            else:
                with cols[i]:
                    st.markdown(
                        f"""
                        <div style="background-color:#f0f0f0; border:2px solid {session_colors[i]}; border-radius:10px; padding:15px; text-align:left;">
                            <h4 style="margin-top:0; margin-bottom:8px; color:{session_colors[i]}; font-weight:bold; font-size:18px;">Best {session} Time</h4>
                            <p style="margin-bottom:0; color:#888888; font-size:18px;">No data available</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
        else:
            with cols[i]:
                st.markdown(
                    f"""
                    <div style="background-color:#f0f0f0; border:2px solid {session_colors[i]}; border-radius:10px; padding:15px; text-align:left;">
                        <h4 style="margin-top:0; margin-bottom:8px; color:{session_colors[i]}; font-weight:bold; font-size:18px;">Best {session} Time</h4>
                        <p style="margin-bottom:0; color:#888888; font-size:18px;">No data available</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

def display_qualifying_comparison(quali_display, data, race_id=None):
    """Display qualifying time comparison between two drivers"""
    
    # Get all drivers with their full names and sort by fastest Q3 time (or Q2, then Q1)
    all_drivers = quali_display[['driverId', 'forename', 'surname', 'code', 'q1', 'q2', 'q3']].copy()
    all_drivers = all_drivers.drop_duplicates()
    
    # Create driver options with full names, sorted by fastest time
    driver_options = []
    driver_mapping = {}
    
    # Calculate best time for each driver for sorting
    for _, row in all_drivers.iterrows():
        full_name = f"{row['forename']} {row['surname']}"
        surname = row['surname']
        code = row['code'] if pd.notna(row['code']) else f"{row['forename'][:3].upper()}"
        
        # Find best time (Q3 > Q2 > Q1)
        best_time = None
        for session in ['q3', 'q2', 'q1']:
            if pd.notna(row[session]):
                time_seconds = time_to_seconds(row[session])
                if time_seconds is not None:
                    best_time = time_seconds
                    break
        
        driver_options.append({
            'name': full_name,
            'surname': surname,
            'best_time': best_time if best_time is not None else float('inf')
        })
        
        driver_mapping[full_name] = {
            'driverId': row['driverId'],
            'code': code,
            'surname': surname
        }
    
    # Sort by fastest time (ascending)
    driver_options = sorted(driver_options, key=lambda x: x['best_time'])
    driver_names = [d['name'] for d in driver_options]
    
    # Controls row: Session selection and driver dropdowns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_session = st.selectbox("Session:", ["Q1", "Q2", "Q3"], key="session_select")
    
    with col2:
        # First dropdown - fastest driver by default
        selected_driver1 = st.selectbox("Driver 1:", driver_names, index=0, key="driver1_select")
    
    with col3:
        # Second dropdown - second fastest driver by default
        default_index2 = 1 if len(driver_names) > 1 else 0
        selected_driver2 = st.selectbox("Driver 2:", driver_names, index=default_index2, key="driver2_select")
    
    # Get times for selected drivers and session
    st.write("")  # Add some space
    
    session_col = selected_session.lower()
    driver_times = []
    
    for driver_name in [selected_driver1, selected_driver2]:
        if driver_name in driver_mapping:
            driver_info = driver_mapping[driver_name]
            driver_data = quali_display[quali_display['driverId'] == driver_info['driverId']]
            
            if not driver_data.empty:
                driver_row = driver_data.iloc[0]
                time_seconds = time_to_seconds(driver_row[session_col])
                
                if time_seconds is not None:
                    driver_times.append({
                        'name': driver_name,
                        'surname': driver_info['surname'],
                        'code': driver_info['code'],
                        'time': time_seconds,
                        'number': driver_row.get('number_x', driver_row.get('number_y', ''))
                    })
    
    # Sort by fastest time
    driver_times = sorted(driver_times, key=lambda x: x['time'])
    
    # Display cards in one row
    if len(driver_times) == 2:
        col1, col2 = st.columns(2)
        
        for i, driver_info in enumerate(driver_times):
            with [col1, col2][i]:
                # Format driver number
                driver_number = f"#{driver_info['number']}" if pd.notna(driver_info['number']) and driver_info['number'] != '' else ""
                time_formatted = format_time_mmssms(driver_info['time'])
                
                # Get team color for this driver
                driver_data = quali_display[quali_display['driverId'] == driver_mapping[driver_info['name']]['driverId']]
                if not driver_data.empty and race_id:
                    from card_styling import get_driver_team_color_for_race
                    team_color = get_driver_team_color_for_race(driver_data.iloc[0]['driverId'], race_id, data)
                else:
                    team_color = '#808080'
                
                # Create card similar to session best times
                driver_surname = driver_info['name'].split()[-1]  # Get surname
                st.markdown(
                    f"""
                    <div style="background-color:#f8f9fa; border-left: 5px solid {team_color}; border-radius:10px; padding:15px; text-align:left;">
                        <h4 style="margin-top:0; margin-bottom:8px; color:#FF0000; font-weight:bold; font-size:16px;">{selected_session} Time</h4>
                        <h3 style="margin:5px 0; color:#000000; font-weight:bold; font-size:18px;">{driver_number} {driver_surname}</h3>
                        <p style="margin-bottom:0; color:#000; font-size:14px; font-weight:bold;">{time_formatted}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        
        # Time difference - centered single line
        if len(driver_times) == 2:
            gap = driver_times[1]['time'] - driver_times[0]['time']
            gap_formatted = format_time_mmssms(gap)
            st.markdown(
                f"""
                <div style="text-align:center; margin-top:20px;">
                    <h4>TIME DIFFERENCE: {gap_formatted}</h4>
                </div>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.warning(f"No {selected_session} data available for selected drivers.")

def display_qualifying_progression_all_drivers(quali_display, data, race_id=None):
    """Display qualifying progression chart for all drivers"""
    
    # Get only drivers with Q3 times (filter out drivers without Q3)
    drivers_with_q3 = quali_display[quali_display['q3'].notna()]
    
    if not drivers_with_q3.empty:
        # Create progression data only for drivers with Q3 times
        progression_data = []
        
        for _, row in drivers_with_q3.iterrows():
            driver_name = f"{row['forename']} {row['surname']}"
            driver_code = row['code'] if pd.notna(row['code']) else driver_name[:3].upper()
            
            for session in ['Q1', 'Q2', 'Q3']:
                time_seconds = time_to_seconds(row[session.lower()])
                if time_seconds is not None:
                    progression_data.append({
                        'Session': session,
                        'Driver': driver_name,
                        'Driver_Code': driver_code,
                        'Time (s)': time_seconds,
                        'Time_Formatted': format_time_mmssms(time_seconds)
                    })
        
        if progression_data:
            import plotly.express as px
            progression_df = pd.DataFrame(progression_data)
            
            # Create the line chart with title
            fig = px.line(
                progression_df, 
                x='Session', 
                y='Time (s)', 
                color='Driver',
                markers=True,
                title="Qualifying Progression"
            )
            
            # Apply team colors to the chart
            try:
                # Get race ID from the function context - we'll pass it as parameter
                fig = apply_team_colors_to_existing_chart(fig, progression_df, 'Driver', data, race_id)
            except:
                pass
            
            # Format y-axis with custom time formatting
            fig.update_layout(
                height=700,
                yaxis=dict(
                    title="Lap Time",
                    tickmode='array',
                    tickvals=[progression_df['Time (s)'].min() - 0.5, progression_df['Time (s)'].max() + 0.5],
                    ticktext=[format_time_mmssms(progression_df['Time (s)'].min() - 0.5), 
                             format_time_mmssms(progression_df['Time (s)'].max() + 0.5)]
                ),
                xaxis_title="Qualifying Session",
                legend_title="Driver",
                font=dict(size=16),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.02
                )
            )
            
            # Add custom hover template with formatted times
            for i, trace in enumerate(fig.data):
                driver_data = progression_df[progression_df['Driver'] == trace.name]
                formatted_times = driver_data['Time_Formatted'].tolist()
                driver_codes = driver_data['Driver_Code'].tolist()
                
                # Use driver code in hover if available
                display_name = driver_codes[0] if driver_codes else trace.name
                
                fig.data[i].customdata = [[t] for t in formatted_times]
                fig.data[i].hovertemplate = f'<b>{display_name}</b><br>Session: %{{x}}<br>Time: %{{customdata[0]}}<extra></extra>'
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No qualifying progression data available")
    else:
        st.info("No drivers with Q3 times available for progression chart")