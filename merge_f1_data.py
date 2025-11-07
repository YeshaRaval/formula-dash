"""
Merge new F1 data from Kaggle with existing data
This script safely merges new data without deleting existing records
"""

import pandas as pd
import os
from datetime import datetime

# Configuration: Map each file to its primary key column(s)
FILE_CONFIGS = {
    'circuits.csv': ['circuitId'],
    'circuits_updated.csv': ['circuitId'],
    'constructor_results.csv': ['constructorResultsId'],
    'constructor_standings.csv': ['constructorStandingsId'],
    'constructors.csv': ['constructorId'],
    'driver_standings.csv': ['driverStandingsId'],
    'drivers.csv': ['driverId'],
    'lap_times.csv': ['raceId', 'driverId', 'lap'],
    'pit_stops.csv': ['raceId', 'driverId', 'stop'],
    'qualifying.csv': ['qualifyId'],
    'races.csv': ['raceId'],
    'results.csv': ['resultId'],
    'seasons.csv': ['year'],
    'sprint_results.csv': ['sprintResultId'],
    'status.csv': ['statusId'],
}

def backup_existing_data(data_dir='f1_data'):
    """Create backup of existing data"""
    backup_dir = f"{data_dir}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            src = os.path.join(data_dir, filename)
            dst = os.path.join(backup_dir, filename)
            pd.read_csv(src).to_csv(dst, index=False)
    
    print(f"✓ Backup created: {backup_dir}")
    return backup_dir

def merge_csv_files(existing_file, new_file, primary_keys, output_file):
    """
    Merge two CSV files based on primary keys
    - Keeps all existing records
    - Adds new records from new file
    - Updates existing records if they appear in new file
    """
    try:
        # Read both files
        existing_df = pd.read_csv(existing_file, na_values=['\\N'])
        new_df = pd.read_csv(new_file, na_values=['\\N'])
        
        print(f"  Existing records: {len(existing_df)}")
        print(f"  New file records: {len(new_df)}")
        
        # Check if primary keys exist in both dataframes
        for key in primary_keys:
            if key not in existing_df.columns or key not in new_df.columns:
                print(f"  ⚠ Warning: Primary key '{key}' not found. Using simple append.")
                merged_df = pd.concat([existing_df, new_df], ignore_index=True).drop_duplicates()
                merged_df.to_csv(output_file, index=False)
                print(f"  Merged records: {len(merged_df)}")
                return
        
        # Merge: keep all existing, add new, update duplicates with new data
        merged_df = pd.concat([new_df, existing_df], ignore_index=True)
        merged_df = merged_df.drop_duplicates(subset=primary_keys, keep='first')
        
        # Sort by primary keys for consistency
        merged_df = merged_df.sort_values(by=primary_keys).reset_index(drop=True)
        
        # Save merged data
        merged_df.to_csv(output_file, index=False)
        
        new_records = len(merged_df) - len(existing_df)
        print(f"  Merged records: {len(merged_df)} (+{new_records} new)")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")

def merge_all_data(existing_dir='f1_data', new_dir='f1_data_new', output_dir='f1_data'):
    """
    Merge all CSV files from new directory into existing directory
    """
    if not os.path.exists(new_dir):
        print(f"✗ New data directory '{new_dir}' not found!")
        print(f"  Please download data from Kaggle and extract to '{new_dir}' folder")
        return
    
    # Create backup first
    backup_dir = backup_existing_data(existing_dir)
    
    print(f"\nMerging data from '{new_dir}' into '{output_dir}'...\n")
    
    # Process each configured file
    for filename, primary_keys in FILE_CONFIGS.items():
        existing_file = os.path.join(existing_dir, filename)
        new_file = os.path.join(new_dir, filename)
        output_file = os.path.join(output_dir, filename)
        
        # Skip if file doesn't exist in new data
        if not os.path.exists(new_file):
            print(f"⊘ {filename}: Not found in new data, skipping")
            continue
        
        # If existing file doesn't exist, just copy the new one
        if not os.path.exists(existing_file):
            print(f"+ {filename}: New file, copying...")
            pd.read_csv(new_file).to_csv(output_file, index=False)
            continue
        
        print(f"⟳ {filename}:")
        merge_csv_files(existing_file, new_file, primary_keys, output_file)
    
    print(f"\n✓ Merge complete!")
    print(f"  Backup saved at: {backup_dir}")
    print(f"  Merged data in: {output_dir}")

if __name__ == "__main__":
    print("=" * 60)
    print("F1 Data Merger")
    print("=" * 60)
    print("\nInstructions:")
    print("1. Download latest data from Kaggle")
    print("2. Extract CSV files to 'f1_data_new' folder")
    print("3. Run this script to merge with existing data\n")
    
    # Check if new data directory exists
    if os.path.exists('f1_data_new'):
        merge_all_data()
    else:
        print("✗ 'f1_data_new' folder not found!")
        print("\nPlease create 'f1_data_new' folder and add your new CSV files there.")
        print("Then run this script again.")
