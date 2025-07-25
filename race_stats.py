"""Race statistics display functions"""

import streamlit as st
import pandas as pd
from card_styling import get_driver_team_color_for_race

def clean_display_value(value):
    """Clean display values by replacing \\N with -"""
    if pd.isna(value) or value == '\\N' or value == 'N' or str(value) == 'nan':
        return '-'
    return str(value)


def display_race_stats(race_results, data):
    """Display race winner, pole position, fastest lap, and fastest pitstop cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    # Race Winner Card
    with col1:
        display_winner_card(race_results, data)
    
    # Pole Position Card
    with col2:
        display_pole_position_card(race_results, data)
    
    # Fastest Lap Card
    with col3:
        display_fastest_lap_card(race_results, data)
    
    # Fastest Pitstop Card
    with col4:
        display_fastest_pitstop_card(race_results, data)

def display_winner_card(race_results, data):
    """Display race winner card with team color background"""
    try:
        race_results_copy = race_results.copy()
        race_results_copy['position_num'] = pd.to_numeric(race_results_copy['position'], errors='coerce')
        winner = race_results_copy[race_results_copy['position_num'] == 1]
        
        if not winner.empty:
            winner_row = winner.iloc[0]
            race_number = winner_row['number'] if pd.notna(winner_row['number']) else None
            winner_data = winner.merge(data['drivers'], on='driverId', how='left').iloc[0]
            
            driver_number = f"#{int(race_number)}" if race_number is not None else ""
            driver_name = winner_data['surname']
            race_time = winner_data['time'] if pd.notna(winner_data['time']) else 'N/A'
            
            # Get team color
            race_id = winner_row['raceId']
            driver_id = winner_row['driverId']
            team_color = get_driver_team_color_for_race(driver_id, race_id, data)
            
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid {team_color}; height: 150px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; overflow: hidden;">
                <h4 style="color: #FF0000; margin: 0; font-weight: bold; font-size: 14px; line-height: 1.2;">🏆 Race Winner</h4>
                <h3 style="color: #000; margin: 0; font-size: 16px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{driver_number} {driver_name}</h3>
                <p style="color: #000; margin: 0; font-size: 14px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: bold;">{race_time}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            raise Exception("No winner found")
    except:
        display_no_data_card("🏆 Race Winner")

def display_pole_position_card(race_results, data):
    """Display pole position card with team color background"""
    try:
        qualifying_data = pd.read_csv('f1_data/qualifying.csv')
        race_id = race_results['raceId'].iloc[0] if not race_results.empty else None
        
        if race_id is not None:
            pole_qualifying = qualifying_data[
                (qualifying_data['raceId'] == race_id) & 
                (qualifying_data['position'] == 1)
            ]
            
            if not pole_qualifying.empty:
                pole_row = pole_qualifying.iloc[0]
                race_number = pole_row['number'] if pd.notna(pole_row['number']) else None
                pole_data = pole_qualifying.merge(data['drivers'], on='driverId', how='left').iloc[0]
                
                driver_number = f"#{int(race_number)}" if race_number is not None else ""
                driver_name = pole_data['surname']
                
                q_times = [pole_data['q1'], pole_data['q2'], pole_data['q3']]
                valid_times = [t for t in q_times if pd.notna(t)]
                best_time = min(valid_times) if valid_times else 'N/A'
                
                # Get team color
                driver_id = pole_row['driverId']
                team_color = get_driver_team_color_for_race(driver_id, race_id, data)
                
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid {team_color}; height: 150px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; overflow: hidden;">
                    <h4 style="color: #FF0000; margin: 0; font-weight: bold; font-size: 14px; line-height: 1.2;">🥇 Pole Position</h4>
                    <h3 style="color: #000; margin: 0; font-size: 16px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{driver_number} {driver_name}</h3>
                    <p style="color: #000; margin: 0; font-size: 14px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: bold;">{best_time}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                raise Exception("No qualifying data")
        else:
            raise Exception("No race ID")
    except:
        # Fallback to grid position 1
        pole = race_results[race_results['grid'] == 1] if 'grid' in race_results.columns else race_results.head(1)
        if not pole.empty:
            pole_row = pole.iloc[0]
            pole_data = pole.merge(data['drivers'], on='driverId', how='left').iloc[0]
            driver_number = f"#{int(pole_data['number'])}" if 'number' in pole_data.index and pd.notna(pole_data['number']) else ""
            driver_name = pole_data['surname']
            grid_pos = f"Grid: {pole_data['grid']}" if pd.notna(pole_data['grid']) else 'N/A'
            
            # Get team color
            race_id = pole_row['raceId']
            driver_id = pole_row['driverId']
            team_color = get_driver_team_color_for_race(driver_id, race_id, data)
            
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid {team_color}; height: 150px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; overflow: hidden;">
                <h4 style="color: #FF0000; margin: 0; font-weight: bold; font-size: 14px; line-height: 1.2;">🥇 Pole Position</h4>
                <h3 style="color: #000; margin: 0; font-size: 16px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{driver_number} {driver_name}</h3>
                <p style="color: #000; margin: 0; font-size: 14px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: bold;">{grid_pos}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            display_no_data_card("🥇 Pole Position")

def display_fastest_lap_card(race_results, data):
    """Display fastest lap card with team color background"""
    try:
        race_results_copy = race_results.copy()
        race_results_copy['position_num'] = pd.to_numeric(race_results_copy['position'], errors='coerce')
        
        top_10_drivers = race_results_copy[
            (race_results_copy['position_num'] >= 1) & 
            (race_results_copy['position_num'] <= 10) & 
            (race_results_copy['fastestLapTime'].notna())
        ]
        
        if not top_10_drivers.empty:
            top_10_copy = top_10_drivers.copy()
            top_10_copy['fastestLapTime_seconds'] = top_10_copy['fastestLapTime'].apply(time_to_seconds)
            top_10_copy = top_10_copy[top_10_copy['fastestLapTime_seconds'] != float('inf')]
            
            if not top_10_copy.empty:
                fastest_idx = top_10_copy['fastestLapTime_seconds'].idxmin()
                fastest_data = top_10_copy.loc[fastest_idx]
                
                race_number = fastest_data['number'] if pd.notna(fastest_data['number']) else None
                fastest_driver = pd.DataFrame([fastest_data]).merge(data['drivers'], on='driverId', how='left').iloc[0]
                
                driver_number = f"#{int(race_number)}" if race_number is not None else ""
                driver_name = fastest_driver['surname']
                lap_time = fastest_data['fastestLapTime'] if pd.notna(fastest_data['fastestLapTime']) else 'N/A'
                
                # Get team color
                race_id = fastest_data['raceId']
                driver_id = fastest_data['driverId']
                team_color = get_driver_team_color_for_race(driver_id, race_id, data)
                
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid {team_color}; height: 150px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; overflow: hidden;">
                    <h4 style="color: #FF0000; margin: 0; font-weight: bold; font-size: 14px; line-height: 1.2;">⚡ Fastest Lap</h4>
                    <h3 style="color: #000; margin: 0; font-size: 16px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{driver_number} {driver_name}</h3>
                    <p style="color: #000; margin: 0; font-size: 14px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: bold;">{lap_time}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                raise Exception("No valid fastest lap data in top 10")
        else:
            raise Exception("No fastest lap data for top 10 drivers")
    except:
        display_no_data_card("⚡ Fastest Lap")

def display_fastest_pitstop_card(race_results, data):
    """Display fastest pitstop card with team color background"""
    try:
        # Try to load pit stops data
        pit_stops = pd.read_csv('f1_data/pit_stops.csv')
        race_id = race_results['raceId'].iloc[0] if not race_results.empty else None
        
        if race_id is not None:
            race_pit_stops = pit_stops[pit_stops['raceId'] == race_id]
            
            if not race_pit_stops.empty:
                # Find fastest pit stop
                fastest_pit_idx = race_pit_stops['milliseconds'].idxmin()
                fastest_pit = race_pit_stops.loc[fastest_pit_idx]
                
                # Get driver info
                pit_driver = data['drivers'][data['drivers']['driverId'] == fastest_pit['driverId']]
                if not pit_driver.empty:
                    driver_data = pit_driver.iloc[0]
                    driver_name = driver_data['surname']
                    
                    # Get driver number from race results
                    driver_result = race_results[race_results['driverId'] == fastest_pit['driverId']]
                    driver_number = ""
                    if not driver_result.empty and pd.notna(driver_result.iloc[0]['number']):
                        driver_number = f"#{int(driver_result.iloc[0]['number'])}"
                    
                    # Format pit stop time
                    pit_time_seconds = fastest_pit['milliseconds'] / 1000
                    pit_time = f"{pit_time_seconds:.3f}s"
                    
                    # Get team color
                    driver_id = fastest_pit['driverId']
                    team_color = get_driver_team_color_for_race(driver_id, race_id, data)
                    
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid {team_color}; height: 150px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; overflow: hidden;">
                        <h4 style="color: #FF0000; margin: 0; font-weight: bold; font-size: 14px; line-height: 1.2;">🏎️ Fastest Pitstop</h4>
                        <h3 style="color: #000; margin: 0; font-size: 16px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{driver_number} {driver_name}</h3>
                        <p style="color: #000; margin: 0; font-size: 14px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: bold;">{pit_time}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    raise Exception("No driver data for fastest pit stop")
            else:
                raise Exception("No pit stop data")
        else:
            raise Exception("No race ID")
    except:
        display_no_data_card("🏎️ Fastest Pitstop")

def display_no_data_card(title):
    """Display a no data available card with consistent sizing"""
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #FF0000; height: 150px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; overflow: hidden;">
        <h4 style="color: #FF0000; margin: 0; font-weight: bold; font-size: 14px; line-height: 1.2;">{title}</h4>
        <h3 style="color: #000; margin: 0; font-size: 16px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">N/A</h3>
        <p style="color: #000; margin: 0; font-size: 14px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: bold;">No data available</p>
    </div>
    """, unsafe_allow_html=True)

def time_to_seconds(time_str):
    """Convert time string to seconds for comparison"""
    if pd.isna(time_str):
        return float('inf')
    try:
        if ':' in str(time_str):
            parts = str(time_str).split(':')
            minutes = float(parts[0])
            seconds = float(parts[1])
            return minutes * 60 + seconds
        else:
            return float(time_str)
    except:
        return float('inf')