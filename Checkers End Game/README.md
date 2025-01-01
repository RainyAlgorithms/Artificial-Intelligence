# Checkers Endgame Puzzle Solver

This project implements a solver for Checkers endgame puzzles using **Game Tree Search (GTS)** techniques, including **alpha-beta pruning**, **state caching**, and **node ordering**. The solver ensures optimal moves for both players while minimizing or maximizing the number of moves as required.

## Features

- **Game Simulation:** Simulates Standard English Draughts rules, including:
  - Piece movements (normal and king).
  - Mandatory and multi-jumps.
  - Endgame conditions.
- **Algorithms:**
  - **Alpha-Beta Pruning** for efficient game tree exploration.
  - **Evaluation Function** for non-terminal state utility estimation.
  - **Depth-Limited Search** with iterative deepening to optimize performance.
- **Optimal Play:** Ensures red wins in the minimum number of moves while black plays adversarially to prolong the game.

## Usage

Run the solver on a Checkers endgame input file using the following command:

```bash
python3 checkers.py --inputfile <input file> --outputfile <output file>
```

### Example
```bash
python3 checkers.py --inputfile puzzle1.txt --outputfile solution1.txt
```

### Input File Format
- The board is represented as an 8x8 grid with the following characters:
  - `.`: Empty square
  - `r`: Red piece
  - `R`: Red king
  - `b`: Black piece
  - `B`: Black king
- Example state:
  ```
  ........
  ....b...
  .......R
  ..b.b...
  ...b...r
  ........
  ...r....
  ....B...
  ```

### Output File
- If solvable: The sequence of game states from the initial state to the game's end, separated by an empty line.
- Example output:
  ```
  ........
  ....b...
  .......R
  ..b.b...
  ...b...r
  ........
  ...r....
  ....B...

  (next state)

  ```

## Key Classes and Functions

- **`State`**: Represents the Checkers board and its properties.
- **`find_possible_moves`**: Generates legal moves for a given player.
- **`alpha_beta`**: Implements alpha-beta pruning with depth limits.
- **`evaluate`**: Estimates utility for non-terminal states.
- **`gts`**: Combines iterative deepening and alpha-beta pruning to compute the solution.

## Requirements

- Python 3.x

## Notes

- The program adheres to a 4-minute time limit for solving each puzzle.
- For optimal performance, test on the specified server.
