"""
This script is used to annotate a PGN file with Stockfish evaluations.
"""
import chess
import chess.engine
import chess.pgn
import os
import time
from pathlib import Path


def analyze_game_with_stockfish(file_path, stockfish_path, depth, output_directory):
    scores = []  # Create an empty list to store cp_values or mate_values

    # Open and read the PGN file
    with open(file_path) as pgn:
        try:
            game = chess.pgn.read_game(pgn)
        except ValueError:
            print(f"Error reading game from {file_path} - it may have an invalid PGN string.")
            return

        if game is None:
            print(f"The PGN file {file_path} is empty or not valid.")
            return

        # Set up the Stockfish engine
        with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
            # Iterate over the nodes and analyze the positions
            node = game
            while node.variations:
                next_node = node.variations[0]
                board = next_node.board()
                info = engine.analyse(board, chess.engine.Limit(depth=depth))
                score = info.get("score", None)
                if score is not None:
                    cp = score.relative.score(mate_score=10000)
                    # Convert cp to pawn units and adjust sign for black
                    evaluation = cp / 100.0
                    if not board.turn:
                        evaluation *= -1

                    scores.append(evaluation)
                node = next_node

    # Call the function to annotate the game with the scores
    annotate_game_with_scores(file_path, scores, output_directory)


def annotate_game_with_scores(file_path, scores, output_directory):
    # Open and read the PGN file
    with open(file_path) as pgn:
        try:
            game = chess.pgn.read_game(pgn)
        except ValueError:
            print("Error reading game - it may have an invalid PGN string.")
            return

        if game is None:
            print("The PGN file is empty or not valid.")
            return

        # Iterate over the nodes and add the scores as comments
        node = game
        score_index = 0
        while node.variations:
            next_node = node.variations[0]
            if score_index < len(scores):
                score = scores[score_index]
                eval_string = str(score)
                if isinstance(score, str) and "mate" in score:
                    eval_string = f"[{score}]"
                else:
                    eval_string = f"[%eval {eval_string}]"
                next_node.comment = eval_string
            node = next_node
            score_index += 1

        # Construct the output file path
        relative_path = Path(file_path).relative_to(dir_path)
        dest_folder = Path(output_directory) / relative_path.parent
        dest_folder.mkdir(parents=True, exist_ok=True)
        base_name, _ = os.path.splitext(os.path.basename(file_path))
        output_file_path = dest_folder / f"{base_name}.pgn"

        # Write the annotated PGN
        with open(output_file_path, 'w') as annotated_pgn:
            exporter = chess.pgn.FileExporter(annotated_pgn)
            game.accept(exporter)

def main():
    # Current Time
    start_time = time.time()

    # Depth to analyze each position (change this value as needed)
    DEPTH = 20
    
    # Set the paths
    input_dir_path = ''
    output_directory = ''
    # e.g.: 'C:\...\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe'
    stockfish_path = ''

    # Walk through the directory including all subdirectories
    for subdir, dirs, files in os.walk(input_dir_path):
        for file in files:
            if file.endswith(".pgn"):
                file_path = os.path.join(subdir, file)
                analyze_game_with_stockfish(file_path, stockfish_path, DEPTH, output_directory)

    end_time = time.time()
    print("Script finished in {:.2f} minutes".format((end_time - start_time) / 60.0))

if __name__ == "__main__":
    main()
