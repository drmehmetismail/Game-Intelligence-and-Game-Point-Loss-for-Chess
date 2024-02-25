# Game-Intelligence-for-Chess
For quick calculation of Game Intelligence (GI) and Game Point Loss (GPL) in chess games for a given .PGN file. 

## Scripts
1. `main.py`: main script.
2. `pgn_evaluation_fast_analyzer.py`: Analyzes Stockfish-annotated PGN files and outputs a JSON file with the stats.
3. `stockfish_pgn_annotator.py`: Annotates PGN files with Stockfish evaluations and outputs the annotated PGN.

## Reference
- For more information, see https://doi.org/10.48550/arXiv.2302.13937
- For World Championship and super GM games, see https://github.com/drmehmetismail/Performance-Metrics
- For Engine vs Engine games (CCRL), see https://github.com/drmehmetismail/Engine-vs-engine-chess-stats
- For Lichess games, see https://github.com/drmehmetismail/Chess-Data-Processing

## Citation
Please cite the following paper if you find this helpful.
```
@article{ismail2023human,
  title={Human and Machine: Practicable Mechanisms for Measuring Performance in Partial Information Games},
  author={Ismail, Mehmet S},
  journal={arXiv preprint arXiv:2302.13937},
  year={2023}
}
```
