import sys
import argparse


class BattleshipCSP:
    def __init__(self, rows, cols, ships, board):
        self.rows = rows  # Row constraints
        self.cols = cols  # Column constraints
        self.N = len(board)  # Size of the NxN board
        self.ships = ships  # Number of ships (submarines, destroyers, cruisers, battleships, carriers)
        self.board = board  # Initial board state

        # Possible ship orientations
        self.ship_orientations = {
            1: ['S'],  # Submarine
            2: ['<', '>'],  # Destroyer (horizontal), ['^', 'v'] for vertical destroyers
            3: ['^', 'v'],  # Cruiser (vertical)
            4: ['M'],  # Middle of ships like Battleships
        }

        # Variables and their domains (water or ship parts)
        self.variables = [(r, c) for r in range(self.N) for c in range(self.N)]
        self.domains = self.preprocess()
        self.domains = self.preprocess()

    def preprocess(self):
        """ Initialize the domain for each variable based on the initial board state. """
        domains = {}

        # Rows to water where the row constraint is 0
        for r in range(self.N):
            if self.rows[r] == 0:
                for c in range(self.N):
                    self.board[r][c] = '.'

        # Columns to water where the column constraint is 0
        for c in range(self.N):
            if self.cols[c] == 0:
                for r in range(self.N):
                    self.board[r][c] = '.'

        # Domains based on the board, applying specific ship rules
        for r in range(self.N):
            for c in range(self.N):
                if self.board[r][c] == 'S':
                    # 1 x 1: Surround with water
                    self.board = self.surround_with_water(r, c)
                    domains[(r, c)] = ['S']

                    # Remove the ship from total number of possible ships in row and column constraints
                    # Remove from total number of left over submarines
                    self.rows[r] -= 1
                    self.cols[r] -= 1
                    self.ships[0] -= 1

                elif self.board[r][c] == 'M':
                    # Middle: Corners should be water
                    self.board = self.set_corners_to_water(r, c)
                    domains[(r, c)] = ['M']
                    # Remove the ship from total number of possible ships in row and column constraints
                    self.rows[r] -= 1
                    self.cols[r] -= 1

                elif self.board[r][c] in ['<', '>', '^', 'v']:
                    # Head pieces: Semi-circle water placement
                    self.board = self.surround_head_with_water(r, c, self.board[r][c])
                    domains[(r, c)] = [self.board[r][c]]
                    # Remove the ship from total number of possible ships in row and column constraints
                    self.rows[r] -= 1
                    self.cols[r] -= 1

                elif self.board[r][c] == '0':  # No hint for that square
                    domains[(r, c)] = ['.', 'S', '<', '>', '^', 'v', 'M']  # Possible ship parts or water

                else:
                    domains[(r, c)] = [self.board[r][c]]  # Already revealed ship or water

        return domains

    # Helper functions

    def surround_with_water(self, r, c):
        """ Surround the submarine 'S' at (r, c) with water. """

        # top-left corner
        if r > 0 and c > 0 and self.board[r - 1][c - 1] == '0':
            self.board[r - 1][c - 1] = '.'

        # top
        if r > 0 and self.board[r - 1][c] == '0':
            self.board[r - 1][c] = '.'

        # top-right corner
        if r > 0 and c < self.N - 1 and self.board[r - 1][c + 1] == '0':
            self.board[r - 1][c + 1] = '.'

        # left
        if c > 0 and self.board[r][c - 1] == '0':
            self.board[r][c - 1] = '.'

        # right
        if c < self.N - 1 and self.board[r][c + 1] == '0':
            self.board[r][c + 1] = '.'

        # bottom-left corner
        if r < self.N - 1 and c > 0 and self.board[r + 1][c - 1] == '0':
            self.board[r + 1][c - 1] = '.'

        # bottom
        if r < self.N - 1 and self.board[r + 1][c] == '0':
            self.board[r + 1][c] = '.'

        # bottom-right corner
        if r < self.N - 1 and c < self.N - 1 and self.board[r + 1][c + 1] == '0':
            self.board[r + 1][c + 1] = '.'

        return self.board

    def set_corners_to_water(self, r, c):
        """ Set the diagonal corners of the middle ship part 'M' to water. """
        # top-left corner
        if r > 0 and c > 0 and self.board[r - 1][c - 1] == '0':
            self.board[r - 1][c - 1] = '.'

        # top-right corner
        if r > 0 and c < self.N - 1 and self.board[r - 1][c + 1] == '0':
            self.board[r - 1][c + 1] = '.'

        # bottom-left corner
        if r < self.N - 1 and c > 0 and self.board[r + 1][c - 1] == '0':
            self.board[r + 1][c - 1] = '.'

        # bottom-right corner
        if r < self.N - 1 and c < self.N - 1 and self.board[r + 1][c + 1] == '0':
            self.board[r + 1][c + 1] = '.'

        return self.board

    def surround_head_with_water(self, r, c, head_type):
        """ Surround the head of the ship with water in a semi-circle. """
        directions = []
        if head_type == '<':  # Left end of a horizontal ship
            # Top, bottom, left, top-left corner, top-right corner, bottom-left corner, bottom-right corner
            directions = [(-1, 0), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        elif head_type == '>':  # Right end of a horizontal ship
            # Top, bottom, left, top-left corner, top-right corner, bottom-left corner, bottom-right corner
            directions = [(-1, 0), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        elif head_type == '^':  # Top end of a vertical ship
            # Left, right, top, top-left corner, top-right corner
            directions = [(0, -1), (0, 1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        elif head_type == 'v':  # Bottom end of a vertical ship
            # Left, right, bottom, top-left corner, top-right corner, bottom-left corner, bottom-right corner
            directions = [(0, -1), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.N and 0 <= nc < self.N:
                if self.board[nr][nc] == '0':
                    self.board[nr][nc] = '.'
        return self.board

    def fc(self, variable):
        pass


def backtrack(csp: BattleshipCSP):
    # Base case: if the CSP is complete, check for solution validity
    if csp.is_complete():
        csp.fill_water()
        
        if csp.is_solved():
            return csp
        csp.clear_water()
        return None

    # Select the next variable to assign
    variable = csp.select_next_variable()

    # Try each value in the variable's domain
    for value in variable.domain:
        if not csp.assign_value(variable, value):
            variable.unassign()
            continue

        # Perform forward checking
        pruned_values = csp.fc(variable)

        # Recursively attempt to solve the CSP
        solution = backtrack(csp)
        if solution:
            return solution

        # Backtrack: undo assignment and restore pruned values
        csp.unassign(variable)
        for affected_var in pruned_values:
            affected_var.restore_domain(variable, value)

    return None



def parse_input():
    """ Parse the input file using argparse and return rows, cols, ships, and board. """
    # Use argparse to get input and output file paths
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that will contain the solution."
    )
    args = parser.parse_args()

    # Open the input file and read its contents
    with open(args.inputfile, 'r') as file:
        b = file.read()

    # Split the file contents into lines
    b2 = b.split()

    # Row constraints (first line)
    rows = list(map(int, b2[0]))

    # Column constraints (second line)
    cols = list(map(int, b2[1]))

    # Ship counts (third line)
    ships = list(map(int, b2[2]))  # Order: Submarines, Destroyers, Cruisers, Battleships, Carriers

    while len(ships) < 5:
        ships.append(0)

    # Initialize the board as a list of strings (grid with padding for boundary handling)
    board = []
    for i in range(3, len(b2)):
        board.append(list(b2[i]))  # No need for padding now, raw board

    return rows, cols, ships, board, args.outputfile


def print_board(board):
    """ Print the board. """
    for row in board:
        print(" ".join(row))


if __name__ == "__main__":
    # Parse input file and get rows, cols, ships, board, and output file path
    rows, cols, ships, board, outputfile = parse_input()

    puzzle = BattleshipCSP(rows, cols, ships, board)

    solution = puzzle.solve()

    # Write solution to outputfile, etc.
    with open(outputfile, 'w') as f:
        f.write('\n')
        for row in puzzle.board:
            f.write(" ".join(row) + '\n')
        f.write('\n')
