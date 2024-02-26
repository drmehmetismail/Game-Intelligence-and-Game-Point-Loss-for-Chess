"""This script inputs the JSON files generated by pgn_evaluation_fast_analyzer.py and outputs a CSV file
containing the following columns:
- White, Black, WhiteElo, BlackElo, WhiteResult, BlackResult, gi, gpl, acpl, white_move_number, black_move_number
"""

import json
import os
import pandas as pd
from pandas import json_normalize

def extract_last_name(full_name):
    if not full_name:
        return ''
    
    if ',' in full_name:
        last_name = full_name.split(',')[0].strip()
    else:
        parts = full_name.split()
        last_name = parts[-1].strip()

    return last_name

def process_json_file(json_file_path, data_list):
    try:
        with open(json_file_path, 'r') as f:
            all_data = json.load(f)
            
            if not all_data:  # Add a check for empty data
                print(f"No data found in {json_file_path}")
                return
            # Iterate through each key in the JSON file
            for key, data in all_data.items():
                white_player = data.get('White', '')
                black_player = data.get('Black', '')

                data['White'] = extract_last_name(white_player)
                data['Black'] = extract_last_name(black_player)

                flattened_data = json_normalize(data)
                data_list.append(flattened_data)

    except Exception as e:
        print(f'Error processing {json_file_path}: {e}')

def main_json_to_csv(directory_path, csv_output_dir):
    data_list = []

    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                json_file_path = os.path.join(root, file)
                process_json_file(json_file_path, data_list)

    if not data_list:  # Check if data_list is empty
        print("No JSON files found or all files are empty.")
        return

    data_frame = pd.concat(data_list, ignore_index=True)

    # Ensure the output directory exists
    if not os.path.exists(csv_output_dir):
        os.makedirs(csv_output_dir)

    # Define the output CSV file path within the output directory
    csv_output_file = os.path.join(csv_output_dir, 'aggregated_game_data.csv')
    data_frame.to_csv(csv_output_file, index=False)
    print(f"Data saved to {csv_output_file}")
