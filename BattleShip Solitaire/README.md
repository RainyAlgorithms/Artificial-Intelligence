# Battleship Solitaire Solver

This project implements a solver for **Battleship Solitaire puzzles** using **Constraint Satisfaction Problem (CSP)** techniques, including **backtracking search**, **forward checking**, and **AC-3 arc consistency**. The solver adheres to Battleship Solitaire rules to find valid solutions efficiently.

## Features

- **Puzzle Representation:** Handles various grid sizes and constraints, including:
  - Row and column constraints for ship parts.
  - Ship placement rules (e.g., no diagonal adjacency, water padding).
- **CSP Techniques:**
  - **Backtracking Search** with constraint propagation.
  - **Heuristics:** Implements Minimum-Remaining-Value and Degree heuristics for variable selection.
  - **Preprocessing:** Automatically identifies water and simplifies constraints to reduce search space.

## Usage

Run the solver on a Battleship Solitaire puzzle input file using the following command:

```bash
python3 battle.py --inputfile <input file> --outputfile <output file>
```

### Example
```bash
python3 battle.py --inputfile puzzle1.txt --outputfile solution1.txt
```

### Input File Format
1. **Constraints:**
   - Line 1: Row constraints (number of ship parts per row).
   - Line 2: Column constraints (number of ship parts per column).
   - Line 3: Ship constraints (number of each type of ship: Submarines, Destroyers, Cruisers, Battleships, Carriers).
2. **Grid:** NxN representation with the following characters:
   - `0`: No hint for the square.
   - `S`: Submarine (1x1 ship).
   - `.`: Water.
   - `<`/`>`: Left/Right end of a horizontal ship.
   - `^`/`v`: Top/Bottom end of a vertical ship.
   - `M`: Middle segment of a ship.

Example input:
```
211222
140212
32100
000000
0000S0
000000
000000
00000.
000000
```

### Output File Format
- An NxN grid representing the solved puzzle, with no `0` characters remaining.
- Example output:
  ```
  <>....
  ....S.
  .^....
  .M...S
  .v.^..
  ...v.S
  ```

## Key Classes and Functions

- **`BattleshipCSP`**: Encodes the Battleship puzzle as a CSP with variables and constraints.
- **`backtrack`**: Implements backtracking search with constraint propagation.
- **`preprocess`**: Pre-fills obvious water cells and simplifies constraints.
- **`fc`**: Applies forward checking for domain pruning during search.

## Requirements

- Python 3.x
- Compatible with the `teach.cs` server.

## Notes

- The program adheres to a 4-minute time limit for solving each puzzle.
- For best results, test on the specified server and create additional input cases for thorough validation.