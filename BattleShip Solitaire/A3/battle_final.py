from __future__ import annotations

import itertools
import argparse
from collections import defaultdict


class Ship:

    def __init__(self, coord, direction: int, length: int, domain):
        self.location = coord
        self.direction = direction
        self.length = length
        self.default_domain = domain.copy()
        self.domain = domain.copy()
        self.pruned = defaultdict(set)
        self.constant_check = False

    def __hash__(self):
        return hash(id(self))


class BattleshipCSP:

    def __init__(self, filename: str):
        self.read_from_file(filename)
        self.preprocess()

    def next_var(self):
        for variables in self.variables[::-1]:
            for variable in variables:
                if not (variable.location != (-1, -1) and variable.direction != -1):
                    return variable

    def surrounded_water_check(self, x: int, y: int, direction=(1, 0)):

        piece = self[x, y]
        directions = []
        if piece == 'S':
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
        elif piece == '^':
            directions = [(1, 0), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
        elif piece == 'v':
            directions = [(1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
        elif piece == '<':
            directions = [(-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
        elif piece == '>':
            directions = [(1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
        elif piece == 'M':
            directions = [(1, 1), (-1, 1), (-1, -1), (1, -1),
                          (direction[1], direction[0]), (-direction[1], direction[0])]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue
            if self[nx, ny] != '.':
                return False
        return True

    def valid_ship_check(self):
        visited_centers = set()
        ship_counts = [0] * len(self.ship_constraints)

        def is_horizontal_ship_valid(start_x, y):

            current_x = start_x + 1
            middle_cords = set()
            while current_x < self.width and self[(next_pos := (current_x, y))] == 'M':
                if not self.surrounded_water_check(current_x, y, (1, 0)):
                    return False, 0
                middle_cords.add(next_pos)
                current_x += 1
            if current_x == self.width or self[current_x, y] != '>':
                return False, 0
            ship_length = current_x - start_x
            if ship_length >= len(self.ship_constraints):
                return False, 0
            visited_centers.update(middle_cords)
            return True, ship_length

        def is_vertical_ship_valid(x, start_y):

            current_y = start_y + 1
            middle_cords = set()
            while current_y < self.height and self[(next_pos := (x, current_y))] == 'M':
                if not self.surrounded_water_check(x, current_y, (0, 1)):
                    return False, 0
                middle_cords.add(next_pos)
                current_y += 1
            if current_y == self.height or self[x, current_y] != 'v':
                return False, 0
            ship_length = current_y - start_y
            if ship_length >= len(self.ship_constraints):
                return False, 0
            visited_centers.update(middle_cords)
            return True, ship_length

        def is_submarine_valid(x, y):

            if not self.surrounded_water_check(x, y):
                return False
            ship_counts[0] += 1
            if ship_counts[0] > self.ship_constraints[0]:
                return False
            return True

        for row in range(self.height):
            for col in range(self.width):
                cell = self[col, row]
                if cell == '0':
                    return False
                if cell == '.':
                    continue
                if cell == 'M' and (col, row) not in visited_centers:
                    return False
                if cell == 'S':
                    if not is_submarine_valid(col, row):
                        return False
                elif cell == '<':
                    valid, length = is_horizontal_ship_valid(col, row)
                    if not valid:
                        return False
                    ship_counts[length] += 1
                    if ship_counts[length] > self.ship_constraints[length]:
                        return False
                elif cell == '^':
                    valid, length = is_vertical_ship_valid(col, row)
                    if not valid:
                        return False
                    ship_counts[length] += 1
                    if ship_counts[length] > self.ship_constraints[length]:
                        return False

        return ship_counts == self.ship_constraints

    def row_col_check(self):
        rows, columns = [0] * self.width, [0] * self.height
        for y in range(self.height):
            for x in range(self.width):
                if (p := self[x, y]) == '0':
                    return False
                if p == '.':
                    continue
                rows[y] += 1
                if rows[y] > self.row_constraints[y]:
                    return False
                columns[x] += 1
                if columns[x] > self.column_constraints[x]:
                    return False
        return rows == self.row_constraints and columns == self.column_constraints

    def get_row_col(self):
        rows, columns = [0] * self.height, [0] * self.width
        for y in range(self.height):
            for x in range(self.width):
                if self[x, y] == '0' or self[x, y] == '.':
                    continue
                rows[y] += 1
                columns[x] += 1
        return rows, columns

    def ship_placement(self, ship_variable: Ship):
        row_usage, col_usage = self.get_row_col()
        start_x, start_y = ship_variable.location
        ship_length = ship_variable.length

        def is_within_bounds(x, y):
            return 0 <= x < self.width and 0 <= y < self.height

        def validate_constraints(delta_rows, delta_cols):
            if any(row_usage[i] + delta_rows[i] > self.row_constraints[i] for i in range(len(delta_rows))):
                return False
            if any(col_usage[i] + delta_cols[i] > self.column_constraints[i] for i in range(len(delta_cols))):
                return False
            return True

        def check_cells_and_update(x, y, dx, dy, head, tail):
            delta_rows = [0] * self.height
            delta_cols = [0] * self.width
            empty_check = False

            if self[x, y] == '0':
                delta_rows[y] += 1
                delta_cols[x] += 1
                empty_check = True
            elif self[x, y] != head:
                return False, delta_rows, delta_cols, empty_check

            for i in range(1, ship_length - 1):
                nx, ny = x + i * dx, y + i * dy
                if not is_within_bounds(nx, ny) or self[nx, ny] not in {'M', '0'}:
                    return False, delta_rows, delta_cols, empty_check
                if self[nx, ny] == '0':
                    delta_rows[ny] += 1
                    delta_cols[nx] += 1
                    empty_check = True

            tail_x, tail_y = x + (ship_length - 1) * dx, y + (ship_length - 1) * dy
            if not is_within_bounds(tail_x, tail_y):
                return False, delta_rows, delta_cols, empty_check
            if self[tail_x, tail_y] == '0':
                delta_rows[tail_y] += 1
                delta_cols[tail_x] += 1
                empty_check = True
            elif self[tail_x, tail_y] != tail:
                return False, delta_rows, delta_cols, empty_check

            return True, delta_rows, delta_cols, empty_check

        if ship_variable.direction == 1:  # Horizontal
            if start_x + ship_length > self.width:
                return False
            valid, delta_rows, delta_cols, has_empty = check_cells_and_update(
                start_x, start_y, dx=1, dy=0, head='<', tail='>')
            if not valid or not has_empty or not validate_constraints(delta_rows, delta_cols):
                return False

        elif ship_variable.direction == 2:  # Vertical
            if start_y + ship_length > self.height:
                return False
            valid, delta_rows, delta_cols, has_empty = check_cells_and_update(
                start_x, start_y, dx=0, dy=1, head='^', tail='v')
            if not valid or not has_empty or not validate_constraints(delta_rows, delta_cols):
                return False

        else:
            if not is_within_bounds(start_x, start_y) or self[start_x, start_y] != '0':
                return False
            if row_usage[start_y] + 1 > self.row_constraints[start_y]:
                return False
            if col_usage[start_x] + 1 > self.column_constraints[start_x]:
                return False

        x, y = ship_variable.location

        if ship_variable.direction == 1:
            self[x, y] = '<'
            for i in range(x + 1, x + ship_variable.length - 1):
                self[i, y] = 'M'
            self[x + ship_variable.length - 1, y] = '>'

        elif ship_variable.direction == 2:
            self[x, y] = '^'
            for i in range(y + 1, y + ship_variable.length - 1):
                self[x, i] = 'M'
            self[x, y + ship_variable.length - 1] = 'v'

        else:
            self[x, y] = 'S'

        return True

    def fc(self, ship_variable):
        start_x, start_y = ship_variable.location
        ship_length = ship_variable.length
        ship_orientation = ship_variable.direction
        restored_variables = set()

        if ship_orientation == 1:  # Horizontal
            ship_cells = [(i, start_y) for i in range(start_x, start_x + ship_length)]
        elif ship_orientation == 2:  # Vertical
            ship_cells = [(start_x, i) for i in range(start_y, start_y + ship_length)]
        else:
            ship_cells = [(start_x, start_y)]

        def get_directions_for_ship(cell_type):

            directions = {
                'S': [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)],
                '<': [(-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)],
                '>': [(1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)],
                '^': [(1, 0), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)],
                'v': [(1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1), (-1, -1), (1, -1)],
                'M': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
            }
            return directions.get(cell_type, [])

        for cell_x, cell_y in ship_cells:
            cell_type = self[cell_x, cell_y]
            surrounding_directions = get_directions_for_ship(cell_type)

            affected_cells = [(cell_x + dx, cell_y + dy) for dx, dy in surrounding_directions]
            affected_cells.extend(ship_cells)

            shrink_domain = set(itertools.product(affected_cells, (0, 1, 2)))

            for variable_group in self.variables:
                for variable in variable_group:
                    if variable.location == (-1, -1) or variable.direction == -1:
                        num = shrink_domain & variable.domain
                        if len(num) != 0:
                            variable.domain -= num
                            variable.pruned[(ship_variable, (ship_variable.location, ship_variable.direction))] |= num
                            restored_variables.add(variable)

        return restored_variables

    def preprocess(self):
        for y in range(self.height):
            for x in range(self.width):
                if (piece := self[x, y]) == '0' or piece == '.':
                    continue
                directions = []
                if piece == 'S':
                    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
                elif piece == '<':
                    directions = [(-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
                    directions.extend([(2, -1), (2, 1)])
                elif piece == '>':
                    directions = [(1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
                    directions.extend([(-2, -1), (-2, 1)])
                elif piece == '^':
                    directions = [(1, 0), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
                    directions.extend([(1, 2), (-1, 2)])
                elif piece == 'v':
                    directions = [(1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
                    directions.extend([(1, -2), (-1, -2)])
                elif piece == 'M':
                    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.width and 0 <= ny < self.height) and self[nx, ny] == '0':
                        self[nx, ny] = '.'

        row_parts, column_parts = self.get_row_col()
        for y in range(self.height):
            if row_parts[y] == self.row_constraints[y]:
                for x in range(self.width):
                    if self[x, y] == '0':
                        self[x, y] = '.'
        for x in range(self.width):
            if column_parts[x] == self.column_constraints[x]:
                for y in range(self.height):
                    if self[x, y] == '0':
                        self[x, y] = '.'

        for y in range(self.height):
            for x in range(self.width):
                piece2 = self[x, y]
                if piece2 in ['0', '<', '^']:
                    continue
                for variables in self.variables:
                    for variable in variables:
                        if not (variable.location != (-1, -1) and variable.direction != -1):
                            variable.default_domain -= {((x, y), 0), ((x, y), 1), ((x, y), 2)}
                            variable.domain = variable.default_domain.copy()
                if piece2 == 'S':
                    for variable in self.variables[0]:
                        if variable.location != (-1, -1) and variable.direction != -1:
                            continue

                        if variable.constant_check:
                            return
                        variable.constant_check = True
                        if (x, y) is None:
                            (x, y) = variable.location
                        else:
                            variable.location = (x, y)

                        variable.direction = 0
                        variable.default_domain = {((x, y), 0)}.copy()
                        variable.domain = variable.default_domain.copy()
                        break

    def read_from_file(self, filename: str):
        with open(filename) as file:
            file_lines = (line.strip() for line in file)
            self.row_constraints = [int(c) for c in next(file_lines)]
            self.column_constraints = [int(c) for c in next(file_lines)]
            self.ship_constraints = [int(c) for c in next(file_lines)]

            self.board = [list(line) for line in file_lines]
            self.original_board = tuple(tuple(line) for line in self.board)
            self.height = len(self.board)
            self.width = len(self.board[0])

            self.variables = []
            all_locations = list(itertools.product(range(self.height), range(self.width)))

            submarine_domain = {(location, 0) for location in all_locations}

            self.variables.append([Ship((-1, -1), -1, 1, submarine_domain)
                                   for _ in range(self.ship_constraints[0])])

            domain = {(location, ship_type) for location in all_locations for ship_type in (1, 2)}

            for i in range(1, len(self.ship_constraints)):
                self.variables.append([Ship((-1, -1), -1, i + 1, domain)
                                       for _ in range(self.ship_constraints[i])])

    def write_output(self, filename):
        with open(filename, 'w') as f:
            for row in self.board:
                f.write(''.join(row) + '\n')
            f.write('\n')

    def __setitem__(self, key, value):
        self.board[key[1]][key[0]] = value

    def __getitem__(self, item):
        return self.board[item[1]][item[0]]


def backtrack(csp: BattleshipCSP):
    if all(all((v.location != (-1, -1) and v.direction != -1) for v in vs) for vs in csp.variables):

        csp.backup_board = [[c for c in row] for row in csp.board]
        for y in range(csp.height):
            for x in range(csp.width):
                if csp[x, y] == '0':
                    csp[x, y] = '.'

        if csp.row_col_check() and csp.valid_ship_check():
            return csp
        csp.board = csp.backup_board
        csp.backup_board = None
        return None
    variable = csp.next_var()
    for val in variable.domain:
        variable.location, variable.direction = val

        if not csp.ship_placement(variable):
            variable.location = (-1, -1)
            variable.direction = -1
            continue
        # fc
        restores = csp.fc(variable)

        result = backtrack(csp)
        if result:
            return result

        # remove ship
        x, y = variable.location
        length = variable.length
        if variable.direction == 1:
            for i in range(x, x + length):
                csp[i, y] = csp.original_board[y][i]
        elif variable.direction == 2:
            for i in range(y, y + length):
                csp[x, i] = csp.original_board[i][x]
        else:
            csp[x, y] = csp.original_board[y][x]

        variable.location = (-1, -1)
        variable.direction = -1

        for restore in restores:
            restore.domain |= restore.pruned[(key := (variable, val))]
            restore.pruned.pop(key)
    return None


if __name__ == '__main__':
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
    args = parser.parse_args()

    puzzle = BattleshipCSP(args.inputfile)
    csp = backtrack(puzzle)

    csp.write_output(args.outputfile)
