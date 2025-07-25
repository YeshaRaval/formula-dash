"""
F1 Team Color Mapping Script
This script creates a comprehensive mapping of F1 team colors based on their official brand colors.
"""

import pandas as pd

# Official F1 team colors (hex codes) - 2024 season and historical teams
TEAM_COLORS = {
    # Current teams (2024)
    'red_bull': '#0600EF',           # Red Bull Racing - Blue
    'ferrari': '#DC143C',            # Ferrari - Red
    'mercedes': '#00D2BE',           # Mercedes - Teal/Turquoise
    'mclaren': '#FF8700',            # McLaren - Orange
    'aston_martin': '#006F62',       # Aston Martin - Green
    'alpine': '#0090FF',             # Alpine - Blue
    'williams': '#005AFF',           # Williams - Blue
    'alphatauri': '#2B4562',         # AlphaTauri - Navy Blue
    'alfa': '#900000',               # Alfa Romeo - Dark Red
    'haas': '#FFFFFF',               # Haas - White (with red accents)
    'sauber': '#00E701',             # Sauber - Green
    'rb': '#6692FF',                 # RB F1 Team - Light Blue
    
    # Historical teams
    'renault': '#FFF500',            # Renault - Yellow
    'toro_rosso': '#469BFF',         # Toro Rosso - Blue
    'force_india': '#FF80C7',        # Force India - Pink
    'racing_point': '#FF80C7',       # Racing Point - Pink
    'lotus_f1': '#FFB800',           # Lotus F1 - Yellow/Gold
    'caterham': '#005030',           # Caterham - Green
    'marussia': '#6E0000',           # Marussia - Dark Red
    'manor': '#6E0000',              # Manor - Dark Red
    'bmw_sauber': '#005AFF',         # BMW Sauber - Blue
    'toyota': '#DC143C',             # Toyota - Red
    'honda': '#FFFFFF',              # Honda - White
    'jaguar': '#004225',             # Jaguar - British Racing Green
    'minardi': '#FFB800',            # Minardi - Yellow
    'jordan': '#FFB800',             # Jordan - Yellow
    'bar': '#FFFFFF',                # BAR - White
    'spyker': '#FF8700',             # Spyker - Orange
    'super_aguri': '#FFFFFF',        # Super Aguri - White
    'lotus_racing': '#FFB800',       # Lotus Racing - Yellow
    'brawn': '#FFFF00',              # Brawn - Yellow
    'benetton': '#0000FF',           # Benetton - Blue
    'tyrrell': '#000080',            # Tyrrell - Navy
    'arrows': '#FF4500',             # Arrows - Orange Red
    'prost': '#0000FF',              # Prost - Blue
    'stewart': '#FFFFFF',            # Stewart - White
    'brabham': '#FFFFFF',            # Brabham - White
    'team_lotus': '#FFB800',         # Team Lotus - Yellow
    'march': '#FF0000',              # March - Red
    'shadow': '#000000',             # Shadow - Black
    'wolf': '#FF0000',               # Wolf - Red
    'hesketh': '#FFFFFF',            # Hesketh - White
    'brm': '#008000',                # BRM - Green
    'matra': '#0000FF',              # Matra - Blue
    'cooper': '#008000',             # Cooper - Green
    'vanwall': '#008000',            # Vanwall - Green
    'maserati': '#FF0000',           # Maserati - Red
    'lancia': '#FF0000',             # Lancia - Red
    'gordini': '#0000FF',            # Gordini - Blue
    'bugatti': '#0000FF',            # Bugatti - Blue
    'porsche': '#000000',            # Porsche - Black
    'bmw': '#0000FF',                # BMW - Blue
    'hrt': '#FF0000',                # HRT - Red
    'virgin': '#FF0000',             # Virgin - Red
    
    # Default fallback colors for any missing teams
    'default': '#808080'             # Gray
}

def create_team_color_mapping():
    """
    Create a comprehensive team color mapping from the constructors CSV
    """
    try:
        # Load constructors data
        constructors_df = pd.read_csv('f1_data/constructors.csv')
        
        # Create color mapping
        color_mapping = {}
        
        for _, row in constructors_df.iterrows():
            constructor_ref = row['constructorRef']
            constructor_name = row['name']
            
            # Map constructor reference to color
            if constructor_ref in TEAM_COLORS:
                color_mapping[constructor_ref] = TEAM_COLORS[constructor_ref]
            else:
                # Use default color for unmapped teams
                color_mapping[constructor_ref] = TEAM_COLORS['default']
                print(f"Warning: No color defined for {constructor_ref} ({constructor_name}), using default gray")
        
        return color_mapping
    
    except Exception as e:
        print(f"Error creating team color mapping: {e}")
        return {}

def get_team_color(constructor_ref):
    """
    Get the hex color code for a specific team
    
    Args:
        constructor_ref (str): The constructor reference (e.g., 'ferrari', 'mercedes')
    
    Returns:
        str: Hex color code
    """
    color_mapping = create_team_color_mapping()
    return color_mapping.get(constructor_ref, TEAM_COLORS['default'])

def get_all_team_colors():
    """
    Get all team colors as a dictionary
    
    Returns:
        dict: Dictionary mapping constructor_ref to hex color
    """
    return create_team_color_mapping()

def save_team_colors_to_csv():
    """
    Save the team color mapping to a CSV file for reference
    """
    try:
        constructors_df = pd.read_csv('f1_data/constructors.csv')
        color_mapping = create_team_color_mapping()
        
        # Add color column to constructors dataframe
        constructors_df['team_color'] = constructors_df['constructorRef'].map(color_mapping)
        
        # Save to new CSV
        constructors_df.to_csv('f1_data/constructors_with_colors.csv', index=False)
        print("Team colors saved to f1_data/constructors_with_colors.csv")
        
        return constructors_df
    
    except Exception as e:
        print(f"Error saving team colors: {e}")
        return None

if __name__ == "__main__":
    # Create and save team color mapping
    print("Creating F1 team color mapping...")
    colors = save_team_colors_to_csv()
    
    if colors is not None:
        print(f"\nSuccessfully mapped colors for {len(colors)} teams")
        print("\nSample team colors:")
        for i, (_, row) in enumerate(colors.head(10).iterrows()):
            print(f"  {row['name']}: {row['team_color']}")
    else:
        print("Failed to create team color mapping")