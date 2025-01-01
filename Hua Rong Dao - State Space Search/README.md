# Hua Rong Dao Puzzle Solver

This project implements a solver for a variant of the Hua Rong Dao (Klotski) tile sliding puzzle using **Depth-First Search (DFS)** and **A* Search** algorithms. The solver aims to transform a given initial puzzle state into a specified goal state.

## Features

- **Puzzle Representation:** Supports 2x2, 1x1, vertical 1x2, and horizontal 1x2 pieces on a 4-column grid of any height.
- **Algorithms:**
  - **DFS:** Explores possible moves to find a solution (not guaranteed optimal).
  - **A* Search:** Uses the Manhattan distance heuristic to find an optimal solution.
- **Output:** Produces a sequence of states leading to the goal or indicates if no solution exists.

## Usage

Run the solver on a puzzle input file using the following commands:

```bash
python3 hrd.py --algo [dfs|astar] --inputfile <input file> --outputfile <output file>
```

### Example
```bash
python3 hrd.py --algo astar --inputfile sample_puzzle.txt --outputfile solution_astar.txt
```

### Input File Format
1. **Initial State:** A grid with characters representing pieces:
   - `.`: Empty space
   - `1`: 2x2 piece
   - `2`: 1x1 piece
   - `<`/`>`: Horizontal 1x2 piece (left/right)
   - `^`/`v`: Vertical 1x2 piece (top/bottom)
2. **Goal State:** Follows the initial state, separated by an empty line.

### Output File
- If solvable: A sequence of puzzle states, separated by empty lines.
- If unsolvable: `No solution`.

## Key Classes

- **`Piece`**: Represents puzzle pieces and their attributes.
- **`Board`**: Represents the puzzle grid and tracks piece positions.
- **`State`**: Wraps a board with additional search-related information (e.g., cost, heuristic).

## Heuristic Function for A*
Uses Manhattan distance to estimate the cost to reach the goal state.

## Requirements

- Python 3.x
- Compatible with the `mcs.utm.utoronto.ca` environment.

## Notes

- Adheres to a 60-second execution limit per puzzle.
- Includes starter code with customizable components for further exploration.

For more details about the traditional Hua Rong Dao puzzle, see [chinesepuzzles.org](http://chinesepuzzles.org/huarong-pass-sliding-block-puzzle/).
