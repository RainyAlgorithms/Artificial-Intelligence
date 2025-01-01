class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board):

        self.board = board

        self.width = 8
        self.height = 8

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")


def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']


def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'


def p_moves(states):
    for state in states:
        print("state display")
        for s in state:
            if isinstance(s, State):
                s.display()


def find_multiple_captures(board, tile, j, i):
    # Return all possible capture sequences
    capture_sequences = []
    if tile == "r":
        if (i > 1 and j > 1 and (board[j - 1][i - 1] in ["b", "B"]) and
                board[j - 2][i - 2] == "."):
            new_board = [row[:] for row in board]
            new_board[j][i] = '.'
            new_board[j - 1][i - 1] = '.'
            if (j - 2) == 0:
                new_board[j - 2][i - 2] = "R"
            else:
                new_board[j - 2][i - 2] = "r"

            capture_state = State(new_board)
            sequence = [capture_state]
            future_sequences = find_multiple_captures(new_board, tile, j - 2, i - 2)

            if future_sequences:
                for future in future_sequences:
                    capture_sequences.append(sequence + future)
            else:
                capture_sequences.append(sequence)

        if (i < 6 and j > 1 and (board[j - 1][i + 1] in ["b", "B"]) and
                board[j - 2][i + 2] == "."):
            new_board = [row[:] for row in board]
            new_board[j][i] = '.'
            new_board[j - 1][i + 1] = '.'
            if (j - 2) == 0:
                new_board[j - 2][i + 2] = "R"
            else:
                new_board[j - 2][i + 2] = "r"

            capture_state = State(new_board)
            sequence = [capture_state]
            future_sequences = find_multiple_captures(new_board, tile, j - 2, i + 2)

            if future_sequences:
                for future in future_sequences:
                    capture_sequences.append(sequence + future)
            else:
                capture_sequences.append(sequence)

    elif tile == "R":
        if (i > 1 and j < 6 and (board[j + 1][i - 1] in ["b", "B"]) and
                board[j + 2][i - 2] == "."):
            new_board = [row[:] for row in board]
            new_board[j][i] = '.'
            new_board[j + 1][i - 1] = '.'
            new_board[j + 2][i - 2] = "R"

            capture_state = State(new_board)
            sequence = [capture_state]
            future_sequences = find_multiple_captures(new_board, tile, j + 2, i - 2)

            if future_sequences:
                for future in future_sequences:
                    capture_sequences.append(sequence + future)
            else:
                capture_sequences.append(sequence)

        if (i < 6 and j < 6 and (board[j + 1][i + 1] in ["b", "B"]) and
                board[j + 2][i + 2] == "."):
            new_board = [row[:] for row in board]
            new_board[j][i] = '.'
            new_board[j + 1][i + 1] = '.'
            new_board[j + 2][i + 2] = "R"

            capture_state = State(new_board)
            sequence = [capture_state]
            future_sequences = find_multiple_captures(new_board, tile, j + 2, i + 2)

            if future_sequences:
                for future in future_sequences:
                    capture_sequences.append(sequence + future)
            else:
                capture_sequences.append(sequence)

        if (i > 1 and j > 1 and (board[j - 1][i - 1] in ["b", "B"]) and
                board[j - 2][i - 2] == "."):
            new_board = [row[:] for row in board]
            new_board[j][i] = '.'
            new_board[j - 1][i - 1] = '.'
            new_board[j - 2][i - 2] = "R"

            capture_state = State(new_board)
            sequence = [capture_state]
            future_sequences = find_multiple_captures(new_board, tile, j - 2, i - 2)

            if future_sequences:
                for future in future_sequences:
                    capture_sequences.append(sequence + future)
            else:
                capture_sequences.append(sequence)

        if (i < 6 and j > 1 and (board[j - 1][i + 1] in ["b", "B"]) and
                board[j - 2][i + 2] == "."):
            new_board = [row[:] for row in board]
            new_board[j][i] = '.'
            new_board[j - 1][i + 1] = '.'
            new_board[j - 2][i + 2] = "R"

            capture_state = State(new_board)
            sequence = [capture_state]
            future_sequences = find_multiple_captures(new_board, tile, j - 2, i + 2)

            if future_sequences:
                for future in future_sequences:
                    capture_sequences.append(sequence + future)
            else:
                capture_sequences.append(sequence)

    elif tile == "b":
        if (i > 1 and j < 6 and (board[j + 1][i - 1] in ["r", "R"]) and
                board[j + 2][i - 2] == "."):

            new_board = [row[:] for row in board]
            new_board[j][i] = '.'
            new_board[j + 1][i - 1] = '.'
            if (j + 2) == 7:
                new_board[j + 2][i - 2] = "B"
            else:
                new_board[j + 2][i - 2] = "b"

            capture_state = State(new_board)
            sequence = [capture_state]
            future_sequences = find_multiple_captures(new_board, tile, j + 2, i - 2)

            if future_sequences:
                for future in future_sequences:
                    capture_sequences.append(sequence + future)
            else:
                capture_sequences.append(sequence)

        if (i < 6 and j < 6 and (board[j + 1][i + 1] in ["r", "R"]) and
                board[j + 2][i + 2] == "."):

            new_board = [row[:] for row in board]
            new_board[j][i] = '.'
            new_board[j + 1][i + 1] = '.'
            if (j + 2) == 7:
                new_board[j + 2][i + 2] = "B"
            else:
                new_board[j + 2][i + 2] = "b"

            capture_state = State(new_board)
            sequence = [capture_state]
            future_sequences = find_multiple_captures(new_board, tile, j + 2, i + 2)

            if future_sequences:
                for future in future_sequences:
                    capture_sequences.append(sequence + future)
            else:
                capture_sequences.append(sequence)

    elif tile == "B":
        if (i > 1 and j < 6 and (board[j + 1][i - 1] in ["r", "R"]) and
                board[j + 2][i - 2] == "."):

            new_board = [row[:] for row in board]
            new_board[j][i] = '.'
            new_board[j + 1][i - 1] = '.'
            new_board[j + 2][i - 2] = "B"

            capture_state = State(new_board)
            sequence = [capture_state]
            future_sequences = find_multiple_captures(new_board, tile, j + 2, i - 2)

            if future_sequences:
                for future in future_sequences:
                    capture_sequences.append(sequence + future)
            else:
                capture_sequences.append(sequence)

        if (i < 6 and j < 6 and (board[j + 1][i + 1] in ["r", "R"]) and
                board[j + 2][i + 2] == "."):

            new_board = [row[:] for row in board]
            new_board[j][i] = '.'
            new_board[j + 1][i + 1] = '.'
            new_board[j + 2][i + 2] = "B"

            capture_state = State(new_board)
            sequence = [capture_state]
            future_sequences = find_multiple_captures(new_board, tile, j + 2, i + 2)

            if future_sequences:
                for future in future_sequences:
                    capture_sequences.append(sequence + future)
            else:
                capture_sequences.append(sequence)

        if (i > 1 and j > 1 and (board[j - 1][i - 1] in ["r", "R"]) and
                board[j - 2][i - 2] == "."):

            new_board = [row[:] for row in board]
            new_board[j][i] = '.'
            new_board[j - 1][i - 1] = '.'
            new_board[j - 2][i - 2] = "B"

            capture_state = State(new_board)
            sequence = [capture_state]
            future_sequences = find_multiple_captures(new_board, tile, j - 2, i - 2)

            if future_sequences:
                for future in future_sequences:
                    capture_sequences.append(sequence + future)
            else:
                capture_sequences.append(sequence)

        if (i < 6 and j > 1 and (board[j - 1][i + 1] in ["r", "R"]) and
                board[j - 2][i + 2] == "."):
            new_board = [row[:] for row in board]
            new_board[j][i] = '.'
            new_board[j - 1][i + 1] = '.'
            new_board[j - 2][i + 2] = "B"

            capture_state = State(new_board)
            sequence = [capture_state]
            future_sequences = find_multiple_captures(new_board, tile, j - 2, i + 2)

            if future_sequences:
                for future in future_sequences:
                    capture_sequences.append(sequence + future)
            else:
                capture_sequences.append(sequence)

    return capture_sequences


def find_possible_moves(state, turn):
    # Return all possible moves for the current player's turn
    if turn == "black":
        player = ["b", "B"]
    else:
        player = ["r", "R"]
    possible_moves = []
    possible_captures = []

    for i in range(state.width):
        for j in range(state.height):
            if state.board[j][i] in player:
                tile = state.board[j][i]
                if tile == "r":
                    capture_sequences = find_multiple_captures(state.board, tile, j, i)
                    if capture_sequences:
                        for capture_state in capture_sequences:
                            possible_captures.append(capture_state[-1])
                    else:
                        if i > 0 and j > 0 and state.board[j - 1][i - 1] == ".":
                            new_board = [row[:] for row in state.board]
                            new_board[j][i] = "."
                            if j - 1 == 0:
                                new_board[j - 1][i - 1] = "R"
                            else:
                                new_board[j - 1][i - 1] = "r"

                            possible_moves.append(State(new_board))

                        if i < 7 and j > 0 and state.board[j - 1][i + 1] == ".":
                            new_board = [row[:] for row in state.board]
                            new_board[j][i] = "."
                            if j - 1 == 0:
                                new_board[j - 1][i + 1] = "R"
                            else:
                                new_board[j - 1][i + 1] = "r"

                            possible_moves.append(State(new_board))
                elif tile == "R":
                    capture_sequences = find_multiple_captures(state.board, tile, j, i)
                    if capture_sequences:
                        for capture_state in capture_sequences:
                            possible_captures.append(capture_state[-1])
                    else:
                        if i > 0 and j < 7 and state.board[j + 1][i - 1] == ".":
                            new_board = [row[:] for row in state.board]
                            new_board[j][i] = "."
                            new_board[j + 1][i - 1] = "R"

                            possible_moves.append(State(new_board))
                        if i < 7 and j < 7 and state.board[j + 1][i + 1] == ".":
                            new_board = [row[:] for row in state.board]
                            new_board[j][i] = "."
                            new_board[j + 1][i + 1] = "R"

                            possible_moves.append(State(new_board))

                        if i > 0 and j > 0 and state.board[j - 1][i - 1] == ".":
                            new_board = [row[:] for row in state.board]
                            new_board[j][i] = "."
                            new_board[j - 1][i - 1] = "R"

                            possible_moves.append(State(new_board))
                        if i < 7 and j > 0 and state.board[j - 1][i + 1] == ".":
                            new_board = [row[:] for row in state.board]
                            new_board[j][i] = "."
                            new_board[j - 1][i + 1] = "R"

                            possible_moves.append(State(new_board))

                elif tile == "b":
                    capture_sequences = find_multiple_captures(state.board, tile, j, i)
                    if capture_sequences:
                        for capture_state in capture_sequences:
                            possible_captures.append(capture_state[-1])
                    else:
                        if i > 0 and j < 7 and state.board[j + 1][i - 1] == ".":
                            new_board = [row[:] for row in state.board]
                            new_board[j][i] = "."
                            if j + 1 == 7:
                                new_board[j + 1][i - 1] = "B"
                            else:
                                new_board[j + 1][i - 1] = "b"

                            possible_moves.append(State(new_board))
                        if i < 7 and j < 7 and state.board[j + 1][i + 1] == ".":
                            new_board = [row[:] for row in state.board]
                            new_board[j][i] = "."
                            if j + 1 == 7:
                                new_board[j + 1][i + 1] = "B"
                            else:
                                new_board[j + 1][i + 1] = "b"

                            possible_moves.append(State(new_board))

                elif tile == "B":
                    capture_sequences = find_multiple_captures(state.board, tile, j, i)
                    if capture_sequences:
                        for capture_state in capture_sequences:
                            possible_captures.append(capture_state[-1])
                    else:
                        if i > 0 and j < 7 and state.board[j + 1][i - 1] == ".":
                            new_board = [row[:] for row in state.board]
                            new_board[j][i] = "."
                            new_board[j + 1][i - 1] = "B"

                            possible_moves.append(State(new_board))
                        if i < 7 and j < 7 and state.board[j + 1][i + 1] == ".":
                            new_board = [row[:] for row in state.board]
                            new_board[j][i] = "."
                            new_board[j + 1][i + 1] = "B"

                            possible_moves.append(State(new_board))

                        if i > 0 and j > 0 and state.board[j - 1][i - 1] == ".":
                            new_board = [row[:] for row in state.board]
                            new_board[j][i] = "."
                            new_board[j - 1][i - 1] = "B"

                            possible_moves.append(State(new_board))
                        if i < 7 and j > 0 and state.board[j - 1][i + 1] == ".":
                            new_board = [row[:] for row in state.board]
                            new_board[j][i] = "."
                            new_board[j - 1][i + 1] = "B"

                            possible_moves.append(State(new_board))

    if possible_captures:
        return possible_captures

    return possible_moves


if __name__ == '__main__':
    initial_board2 = [[".", ".", ".", ".", ".", ".", ".", "."],
                    [".", "b", ".", "b", ".", ".", ".", "."],
                    [".", ".", ".", ".", ".", ".", ".", "."],
                    [".", "b", ".", ".", ".", "b", ".", "."],
                    [".", ".", "r", ".", ".", ".", "R", "."],
                    [".", ".", ".", "r", ".", "b", ".", "."],
                    [".", ".", "B", ".", "b", ".", ".", "."],
                    [".", ".", ".", ".", ".", "r", ".", "."]]

    initial_board4 = [[".", ".", ".", ".", ".", ".", ".", "."],
                    [".", ".", ".", "b", ".", "b", ".", "."],
                    [".", ".", "R", ".", ".", ".", ".", "."],
                    [".", ".", ".", "b", ".", "b", ".", "."],
                    [".", ".", ".", ".", ".", ".", ".", "."],
                    [".", ".", ".", ".", ".", ".", ".", "."],
                    [".", ".", ".", ".", ".", ".", ".", "."],
                    [".", ".", ".", ".", ".", ".", ".", "."]]

    initial_board = [[".", ".", ".", ".", ".", ".", ".", "."],
                     [".", ".", ".", ".", "b", ".", ".", "."],
                     [".", ".", ".", "R", ".", ".", ".", "."],
                     [".", ".", "b", ".", "b", ".", ".", "."],
                     [".", ".", ".", ".", ".", ".", ".", "."],
                     [".", ".", "B", ".", "b", ".", ".", "."],
                     [".", ".", ".", ".", ".", ".", ".", "."],
                     [".", ".", ".", ".", ".", ".", ".", "."]]

    initial_board3 = [[".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", "b", ".", "b", ".", "."],
                      [".", ".", "r", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."],
                      [".", ".", ".", ".", ".", ".", ".", "."]]

    state1 = State(initial_board4)
    print("red")
    for state in find_possible_moves(state1, "red"):
        state.display()
    print("black")
    for state in find_possible_moves(state1, "black"):
        state.display()

    # t = find_possible_moves(state1, "red")
    #
    # print(t)
