# Main function for the Fast GI calculator
from pgn_evaluation_fast_analyzer import main
from stockfish_pgn_annotator import main_stockfish
from csv_to_player_stats import main_stats
from json_to_csv_converter import main_json_to_csv
import time

start_time = time.time()

# If the games are annotated with Stockfish, set this to True
games_annotated = True

if not games_annotated:
    # Set the dir paths for the PGN files and the output directory
    input_dir_path = ''
    output_directory = ''
    # set the path to the Stockfish executable
    # e.g.: 'C:\...\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe'
    stockfish_path = ''
    # Set the depth for the Stockfish analysis
    DEPTH = 20
    # Call the main function to annotate the games
    main_stockfish(input_dir_path, output_directory, stockfish_path, DEPTH)

# Set the input and output directories for the Fast GI calculator
input_pgn_dir = '...'
# Change the output directory if needed
output_json_dir = input_pgn_dir
# Set whether the GI score should be weighted by opponent's Elo
weighted = True
# Input win, draw, and loss values. Standard FIDE: [1, 0.5, 0]. Norway Chess: [3, 1.25, 0] (will be normalized by 1/3; Armageddon score added manually).
wdl_values = [1, 0.5, 0]
main(input_pgn_dir, output_json_dir, wdl_values, weighted)

# Set the input and output directories for the JSON to CSV converter
json_input_dir = '...'
csv_output_dir = '...'
main_json_to_csv(json_input_dir, csv_output_dir)

# Set the input and output directories for the player stats 
#If multiple CSVs set input_dir, otherwise, set csv_all_games_path 
# input_dir = "..."
# csv_all_games_path = combine_csv_files(input_dir, output_filename='combined.csv')
csv_all_games_path = '...'
player_stats_output_dir = '...'
main_stats(csv_all_games_path, player_stats_output_dir)

end_time = time.time()
print("Script finished in {:.2f} minutes".format((end_time - start_time) / 60.0))
