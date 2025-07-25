"""
Enhanced DataFrame styling for F1 Dashboard
"""

import streamlit as st

def apply_dataframe_styles():
    """Apply enhanced styling to all dataframes with larger text and left alignment"""
    st.markdown("""
    <style>
    /* Enhanced DataFrame Styling */
    .dataframe {
        font-size: 25px !important;
        text-align: left !important;
    }
    
    .dataframe th {
        font-size: 25px !important;
        font-weight: bold !important;
        text-align: left !important;
        background-color: #f0f0f0 !important;
        padding: 12px 8px !important;
    }
    
    .dataframe td {
        font-size: 25px !important;
        text-align: left !important;
        padding: 10px 8px !important;
    }
    
    /* Streamlit dataframe specific styling */
    .stDataFrame > div {
        font-size: 25px !important;
    }
    
    .stDataFrame table {
        font-size: 25px !important;
    }
    
    .stDataFrame th {
        font-size: 25px !important;
        font-weight: bold !important;
        text-align: left !important;
        background-color: #f0f0f0 !important;
    }
    
    .stDataFrame td {
        font-size: 25px !important;
        text-align: left !important;
    }
    
    /* Additional styling for better readability */
    .stDataFrame {
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    
    /* Driver card styling for starting grid */
    .driver-card {
        background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
        border: 2px solid #ddd;
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .driver-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .driver-number {
        font-size: 18px;
        font-weight: bold;
        color: #666;
        margin-bottom: 5px;
    }
    
    .driver-name {
        font-size: 22px;
        font-weight: bold;
        color: #000;
        margin: 8px 0;
    }
    
    .driver-team {
        font-size: 16px;
        color: #888;
        margin-top: 5px;
    }
    
    .grid-position {
        position: absolute;
        top: 10px;
        left: 10px;
        background: #ff0000;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

def create_driver_card(position, driver_name, team_name, driver_number="", team_color="#808080"):
    """Create a styled driver card for starting grid"""
    # Format driver number
    number_display = f"#{driver_number}" if driver_number and str(driver_number) != 'nan' else ""
    
    return f"""
    <div class="driver-card" style="border-left: 4px solid {team_color}; position: relative;">
        <div class="grid-position">{position}</div>
        <div class="driver-number">{number_display}</div>
        <div class="driver-name">{driver_name}</div>
        <div class="driver-team">{team_name}</div>
    </div>
    """

def create_starting_grid_layout(grid_data, team_colors):
    """Create a simple starting grid layout using basic Streamlit components"""
    
    # Sort by grid position
    sorted_grid = sorted(grid_data, key=lambda x: x.get('GRID POS.', 999) if x.get('GRID POS.', 999) != '' else 999)
    
    # Create two columns for the grid layout
    col1, col2 = st.columns(2)
    
    # Split drivers into two columns (odd positions left, even positions right)
    left_drivers = []
    right_drivers = []
    
    for driver in sorted_grid:
        pos = driver.get('GRID POS.', 0)
        if pos != '' and pos != 0:
            if pos % 2 == 1:  # Odd positions (1, 3, 5, etc.)
                left_drivers.append(driver)
            else:  # Even positions (2, 4, 6, etc.)
                right_drivers.append(driver)
    
    # Display left column (odd positions)
    with col1:
        st.markdown("##### Odd Grid Positions")
        for driver in left_drivers:
            # Get team color
            team_ref = driver.get('team_ref', 'default')
            team_color = team_colors.get(team_ref, '#808080')
            
            # Extract driver info
            driver_full = driver.get('DRIVER', '')
            driver_number = ""
            driver_name = driver_full
            
            if '#' in driver_full:
                parts = driver_full.split(' ', 1)
                if len(parts) > 1 and parts[0].startswith('#'):
                    driver_number = parts[0][1:]
                    driver_name = parts[1]
            
            # Simple card with colored border
            with st.container():
                st.markdown(f"""
                <div style="border-left: 5px solid {team_color}; background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <div style="color: black;">
                        <strong>P{driver.get('GRID POS.', '')} - #{driver_number} {driver_name}</strong><br>
                        <span style="color: #666;">{driver.get('TEAM', '')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Display right column (even positions)
    with col2:
        st.markdown("##### Even Grid Positions")
        for driver in right_drivers:
            # Get team color
            team_ref = driver.get('team_ref', 'default')
            team_color = team_colors.get(team_ref, '#808080')
            
            # Extract driver info
            driver_full = driver.get('DRIVER', '')
            driver_number = ""
            driver_name = driver_full
            
            if '#' in driver_full:
                parts = driver_full.split(' ', 1)
                if len(parts) > 1 and parts[0].startswith('#'):
                    driver_number = parts[0][1:]
                    driver_name = parts[1]
            
            # Simple card with colored border
            with st.container():
                st.markdown(f"""
                <div style="border-left: 5px solid {team_color}; background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <div style="color: black;">
                        <strong>P{driver.get('GRID POS.', '')} - #{driver_number} {driver_name}</strong><br>
                        <span style="color: #666;">{driver.get('TEAM', '')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)