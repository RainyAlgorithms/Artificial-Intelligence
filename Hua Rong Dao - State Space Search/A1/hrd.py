import argparse
import sys
import heapq

# ====================================================================================

char_single = '2'


class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0

    def insert(self, item):
        # Use a tuple (item.f, count, item) to ensure the heap is ordered by item.f
        heapq.heappush(self.heap, (item.f, self.count, item))
        self.count += 1

    def extract(self):
        # Pop the smallest item from the heap
        return heapq.heappop(self.heap)[2]

    def is_empty(self):
        return len(self.heap) == 0


class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_2_by_2, is_single, coord_x, coord_y, orientation):
        """
        :param is_2_by_2: True if the piece is a 2x2 piece and False otherwise.
        :type is_2_by_2: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param orientation: The orientation of the piece (one of 'h' or 'v')
            if the piece is a 1x2 piece. Otherwise, this is None
        :type orientation: str
        """

        self.is_2_by_2 = is_2_by_2
        self.is_single = is_single
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.orientation = orientation

    def set_coords(self, coord_x, coord_y):
        """
        Move the piece to the new coordinates.

        :param coord: The new coordinates after moving.
        :type coord: int
        """

        self.coord_x = coord_x
        self.coord_y = coord_y

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.is_2_by_2, self.is_single, \
                                       self.coord_x, self.coord_y, self.orientation)


class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, height, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

        self.width = 4
        self.height = height
        self.pieces = pieces

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()

        self.blanks = []

    # customized eq for object comparison.
    def __eq__(self, other):
        if isinstance(other, Board):
            return self.grid == other.grid
        return False

    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_2_by_2:
                self.grid[piece.coord_y][piece.coord_x] = '1'
                self.grid[piece.coord_y][piece.coord_x + 1] = '1'
                self.grid[piece.coord_y + 1][piece.coord_x] = '1'
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = '1'
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = char_single
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = '<'
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = '^'
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'

    def display(self):
        """
        Print out the current board.

        """
        for i, line in enumerate(self.grid):
            for ch in line:
                print(ch, end='')
            print()


class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces.
    State has a Board and some extra information that is relevant to the search:
    heuristic function, f value, current depth and parent.
    """

    def __init__(self, board, depth, g=0, h=0, parent=None):
        """
        :param board: The board of the state.
        :type board: Board
        :param h: The heuristic function.
        :type h: int
        :param f: The f value of current state.
        :type f: int
        :param g: The cost of current state.
        :type g: int
        :param depth: The depth of current state in the search tree.
        :type depth: int
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.h = h
        self.g = g
        self.f = g + h
        self.depth = depth
        self.parent = parent
        self.path = []


def is_goal_state(state):
    """

    :param state: The current state of a board
    :return: Return true iff state is a goal state
    return type: bool
    """
    return state.board == goal_board


def heuristic(the_board, the_goal_board):
    """
    Calculate the heuristic value for the given state using Manhattan distance.

    :param the_board: The current board
    :param the_goal_board: The goal the board
    :return: The heuristic value (h) of the state
    """

    # 0 is 2by2
    # 1 is single
    # 2 vertical
    # 3 horizontal

    distance = 0
    the_pieces = [[], [], [], []]

    for piece in the_goal_board.pieces:
        index = 0 if piece.is_2_by_2 else 1 if piece.is_single else 2 if piece.orientation == "v" else 3
        the_pieces[index].append(piece)

    for piece in the_board.pieces:
        if piece.is_2_by_2:
            i, p = find_smallest_manhattan_distance(piece.coord_x, piece.coord_y, the_pieces[0])
            the_pieces[0].remove(p)
            distance += i
        elif piece.is_single:
            i, p = find_smallest_manhattan_distance(piece.coord_x, piece.coord_y, the_pieces[1])
            the_pieces[1].remove(p)
            distance += i
        elif piece.orientation == "v":
            i, p = find_smallest_manhattan_distance(piece.coord_x, piece.coord_y, the_pieces[2])
            the_pieces[2].remove(p)
            distance += i
        elif piece.orientation == "h":
            i, p = find_smallest_manhattan_distance(piece.coord_x, piece.coord_y, the_pieces[3])
            the_pieces[3].remove(p)
            distance += i

    return distance


def find_smallest_manhattan_distance(x, y, lst):
    the_min = float("inf")
    piece = None

    for i in lst:
        distance = abs(x - i.coord_x) + abs(y - i.coord_y)
        if distance < the_min:
            the_min = distance
            piece = i

    return the_min, piece


def generate_successors(state, the_goal_board):
    successors = []

    for piece in state.board.pieces:
        coordinate = (piece.coord_x, piece.coord_y)
        if piece.is_2_by_2:
            if (coordinate[1] + 2 < len(state.board.grid) and
                    coordinate[0] < len(state.board.grid[0]) and
                    coordinate[0] + 1 < len(state.board.grid[0]) and
                    state.board.grid[coordinate[1] + 2][coordinate[0]] == "." and
                    state.board.grid[coordinate[1] + 2][coordinate[0] + 1] == "."):
                successors.append(do_the_move(state, piece, "d", the_goal_board))
            if (coordinate[1] - 1 >= 0 and
                    coordinate[0] < len(state.board.grid[0]) and
                    coordinate[0] + 1 < len(state.board.grid[0]) and
                    state.board.grid[coordinate[1] - 1][coordinate[0]] == "." and
                    state.board.grid[coordinate[1] - 1][coordinate[0] + 1] == "."):
                successors.append(do_the_move(state, piece, "u", the_goal_board))
            if (coordinate[1] < len(state.board.grid) and
                    coordinate[0] + 2 < len(state.board.grid[0]) and
                    coordinate[1] + 1 < len(state.board.grid) and
                    state.board.grid[coordinate[1]][coordinate[0] + 2] == "." and
                    state.board.grid[coordinate[1] + 1][coordinate[0] + 2] == "."):
                successors.append(do_the_move(state, piece, "r", the_goal_board))
            if (coordinate[1] < len(state.board.grid) and
                    coordinate[0] - 1 >= 0 and
                    coordinate[1] + 1 < len(state.board.grid) and
                    state.board.grid[coordinate[1]][coordinate[0] - 1] == "." and
                    state.board.grid[coordinate[1] + 1][coordinate[0] - 1] == "."):
                successors.append(do_the_move(state, piece, "l", the_goal_board))
        elif piece.is_single:
            if (coordinate[1] + 1 < len(state.board.grid) and
                    state.board.grid[coordinate[1] + 1][coordinate[0]] == "."):
                successors.append(do_the_move(state, piece, "d", the_goal_board))
            if (coordinate[1] - 1 >= 0 and
                    state.board.grid[coordinate[1] - 1][coordinate[0]] == "."):
                successors.append(do_the_move(state, piece, "u", the_goal_board))
            if (coordinate[0] + 1 < len(state.board.grid[0]) and
                    state.board.grid[coordinate[1]][coordinate[0] + 1] == "."):
                successors.append(do_the_move(state, piece, "r", the_goal_board))
            if (coordinate[0] - 1 >= 0 and
                    state.board.grid[coordinate[1]][coordinate[0] - 1] == "."):
                successors.append(do_the_move(state, piece, "l", the_goal_board))
        elif piece.orientation == "h":
            if (coordinate[1] + 1 < len(state.board.grid) and
                    coordinate[0] < len(state.board.grid[0]) and
                    coordinate[0] + 1 < len(state.board.grid[0]) and
                    state.board.grid[coordinate[1] + 1][coordinate[0]] == "." and
                    state.board.grid[coordinate[1] + 1][coordinate[0] + 1] == "."):
                successors.append(do_the_move(state, piece, "d", the_goal_board))
            if (coordinate[1] - 1 >= 0 and
                    coordinate[0] < len(state.board.grid[0]) and
                    coordinate[0] + 1 < len(state.board.grid[0]) and
                    state.board.grid[coordinate[1] - 1][coordinate[0]] == "." and
                    state.board.grid[coordinate[1] - 1][coordinate[0] + 1] == "."):
                successors.append(do_the_move(state, piece, "u", the_goal_board))
            if (coordinate[0] + 2 < len(state.board.grid[0]) and
                    state.board.grid[coordinate[1]][coordinate[0] + 2] == "."):
                successors.append(do_the_move(state, piece, "r", the_goal_board))
            if (coordinate[0] - 1 >= 0 and
                    state.board.grid[coordinate[1]][coordinate[0] - 1] == "."):
                successors.append(do_the_move(state, piece, "l", the_goal_board))
        elif piece.orientation == "v":
            if (coordinate[1] + 2 < len(state.board.grid) and
                    state.board.grid[coordinate[1] + 2][coordinate[0]] == "."):
                successors.append(do_the_move(state, piece, "d", the_goal_board))
            if (coordinate[1] - 1 >= 0 and
                    state.board.grid[coordinate[1] - 1][coordinate[0]] == "."):
                successors.append(do_the_move(state, piece, "u", the_goal_board))
            if (coordinate[0] + 1 < len(state.board.grid[0]) and
                    coordinate[1] + 1 < len(state.board.grid) and
                    state.board.grid[coordinate[1]][coordinate[0] + 1] == "." and
                    state.board.grid[coordinate[1] + 1][coordinate[0] + 1] == "."):
                successors.append(do_the_move(state, piece, "r", the_goal_board))
            if (coordinate[0] - 1 >= 0 and
                    coordinate[1] + 1 < len(state.board.grid) and
                    state.board.grid[coordinate[1]][coordinate[0] - 1] == "." and
                    state.board.grid[coordinate[1] + 1][coordinate[0] - 1] == "."):
                successors.append(do_the_move(state, piece, "l", the_goal_board))

    return successors


def do_the_move(state, the_piece, move, the_goal_board):

    pieces2 = []

    for piece in state.board.pieces:
        if piece == the_piece:
            if move == "d":
                pieces2.append(Piece(piece.is_2_by_2, piece.is_single, piece.coord_x, piece.coord_y + 1, piece.orientation))
            elif move == "u":
                pieces2.append(Piece(piece.is_2_by_2, piece.is_single, piece.coord_x, piece.coord_y - 1, piece.orientation))
            elif move == "l":
                pieces2.append(Piece(piece.is_2_by_2, piece.is_single, piece.coord_x - 1, piece.coord_y, piece.orientation))
            elif move == "r":
                pieces2.append(Piece(piece.is_2_by_2, piece.is_single, piece.coord_x + 1, piece.coord_y, piece.orientation))
        else:
            pieces2.append(piece)

    board1 = Board(state.board.height, pieces2)

    return State(board1, state.depth + 1, state.g + 1, heuristic(board1, the_goal_board), state)


def dfs(the_board, the_goal_board):
    s = ""
    state = State(the_board, 0, 0, 0)
    frontier = [state]
    explored = set()

    while frontier:
        curr_state = frontier.pop()
        state_tuple = tuple(map(tuple, curr_state.board.grid))
        s += grid_to_string(curr_state.board.grid) + "\n"  # used to be under line 351
        if state_tuple not in explored:
            explored.add(state_tuple)
            if is_goal_state(curr_state):
                return s
            else:
                for successor in generate_successors(curr_state, the_goal_board):
                    frontier.append(successor)
    return "No solution"


def astar(the_board, the_goal_board):

    state = State(the_board, 0, 0, heuristic(the_board, the_goal_board))

    frontier = PriorityQueue()
    frontier.insert(state)
    state.path = [state.board.grid]
    explored = set()

    while not frontier.is_empty():
        curr_state = frontier.extract()
        state_tuple = tuple(map(tuple, curr_state.board.grid))
        if state_tuple not in explored:
            explored.add(state_tuple)
            if is_goal_state(curr_state):
                return "\n".join(grid_to_string(path) for path in curr_state.path)
            else:
                for successor in generate_successors(curr_state, the_goal_board):
                    successor.path = curr_state.path + [successor.board.grid]
                    frontier.insert(successor)
    return "No solution"


def read_from_file(filename):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    puzzle_file = open(filename, "r")

    line_index = 0
    pieces = []
    final_pieces = []
    final = False
    found_2by2 = False
    finalfound_2by2 = False
    height_ = 0

    for line in puzzle_file:
        height_ += 1
        if line == '\n':
            if not final:
                height_ = 0
                final = True
                line_index = 0
            continue
        if not final:  # initial board
            for x, ch in enumerate(line):
                if ch == '^':  # found vertical piece
                    pieces.append(Piece(False, False, x, line_index, 'v'))
                elif ch == '<':  # found horizontal piece
                    pieces.append(Piece(False, False, x, line_index, 'h'))
                elif ch == char_single:
                    pieces.append(Piece(False, True, x, line_index, None))
                elif ch == '1':
                    if found_2by2 == False:
                        pieces.append(Piece(True, False, x, line_index, None))
                        found_2by2 = True
        else:  # goal board
            for x, ch in enumerate(line):
                if ch == '^':  # found vertical piece
                    final_pieces.append(Piece(False, False, x, line_index, 'v'))
                elif ch == '<':  # found horizontal piece
                    final_pieces.append(Piece(False, False, x, line_index, 'h'))
                elif ch == char_single:
                    final_pieces.append(Piece(False, True, x, line_index, None))
                elif ch == '1':
                    if finalfound_2by2 == False:
                        final_pieces.append(Piece(True, False, x, line_index, None))
                        finalfound_2by2 = True
        line_index += 1

    puzzle_file.close()
    board = Board(height_, pieces)
    goal_board = Board(height_, final_pieces)
    return board, goal_board


def grid_to_string(grid):
    string = ""
    for i, line in enumerate(grid):
        for ch in line:
            string += ch
        string += "\n"
    return string


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )
    args = parser.parse_args()

    # read the board from the file
    board, goal_board = read_from_file(args.inputfile)

    if args.algo == "dfs":
        finalSolution = dfs(board, goal_board)

    elif args.algo == "astar":
        finalSolution = astar(board, goal_board)

    with open(args.outputfile, 'w') as f:
        f.write(finalSolution)
