from util import assert_equals, file_to_array
import numpy as np

# Test Files
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
TEST_INPUT_2 = 'test_input2.txt'
TEST_INPUT_3 = 'test_input3.txt'
TEST_INPUT_4 = 'test_input4.txt'
TEST_INPUT_5 = 'test_input5.txt'
TEST_INPUT_6 = 'test_input6.txt'


# Constants
NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"
DIRECTIONS = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    EAST: (1, 0),
    WEST: (-1, 0),
}
INVERTED_DIRECTIONS = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
}
PIPES = {
    "|": (NORTH, SOUTH),
    "-": (EAST, WEST),
    "L": (NORTH, EAST),
    "J": (NORTH, WEST),
    "7": (SOUTH, WEST),
    "F": (SOUTH, EAST),
    ".": (None, None),              # No Pipe
    "S": (None, None)               # Start, special handling
}


def find_furthest(f):
    grid = [[i for i in list(line)] for line in file_to_array(f)]
    (y, x) = np.argwhere(np.array(grid) == "S").tolist()[0]
    distance = 0
    curr_direction = PIPES[find_start_piece(grid, x, y)][0]
    while True:
        x, y = x + DIRECTIONS[curr_direction][0], y + DIRECTIONS[curr_direction][1]
        distance += 1
        curr_pipe = get_pipe(grid, x, y)
        if curr_pipe == "S":
            break
        curr_direction = PIPES[curr_pipe][0] if PIPES[curr_pipe][1] == INVERTED_DIRECTIONS[curr_direction] \
            else PIPES[curr_pipe][1]
    return int(distance/2)


def find_start_piece(grid, start_x, start_y):
    connections = []
    for direction, in [NORTH, SOUTH, EAST, WEST]:
        (x, y) = DIRECTIONS[direction]
        pipe = get_pipe(grid, start_x + x, start_y + y)
        if pipe is None or pipe == ".":
            continue
        if INVERTED_DIRECTIONS[direction] in PIPES[pipe]:
            connections.append(direction)
    for key in PIPES:
        if PIPES[key] is not None and connections[0] in PIPES[key] and connections[1] in PIPES[key]:
            return key


def get_pipe(grid, x, y):
    if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
        return grid[y][x]
    return None


def find_enclosed(f):
    original_grid = [[i for i in list(line)] for line in file_to_array(f)]
    (y, x) = np.argwhere(np.array(original_grid) == "S").tolist()[0]
    initial_piece = find_start_piece(original_grid, x, y)
    original_grid[y][x] = initial_piece  # Replace for later math
    y *= 2
    x *= 2

    (initial_y, initial_x) = (y, x)
    curr_direction = PIPES[initial_piece][0]
    grid = expand(original_grid)

    connected = set()
    while True:
        x1, y1 = DIRECTIONS[curr_direction]
        x, y = x + x1, y + y1
        curr_pipe = get_pipe(grid, x, y)
        connected.add((x, y))
        if x == initial_x and y == initial_y:
            break
        curr_direction = PIPES[curr_pipe][0] if PIPES[curr_pipe][1] == INVERTED_DIRECTIONS[curr_direction] else PIPES[curr_pipe][1]
    connected = get_outer(grid, connected)
    compressed = list(filter(lambda pair: pair[0] % 2 == 0 and pair[1] % 2 == 0, connected))
    return len(original_grid) * len(original_grid[0]) - len(compressed)


def get_outer(grid, connected):
    max_x, max_y = len(grid[0]), len(grid)
    empty = set()

    # build edges
    for x in range(max_x):
        if (x, 0) not in connected:
            empty.add((x, 0))
        if (x, max_y-1) not in connected:
            empty.add((x, max_y-1))
    for y in range(max_y):
        if (0, y) not in connected:
            empty.add((0, y))
        if (max_x-1, y) not in connected:
            empty.add((max_x-1, y))

    while len(empty) > 0:
        next_empty = set()
        for (x, y) in empty:
            connected.add((x, y))
            for x1, y1 in DIRECTIONS.values():
                new_x = x + x1
                new_y = y + y1
                if 0 < new_x < max_x and 0 < new_y < max_y and (new_x, new_y) not in connected:
                    next_empty.add((new_x, new_y))
        empty = next_empty
    return connected


def expand(grid):
    new_grid_y = []
    for y in range(len(grid)):
        expanded = []
        new_grid_y.append(grid[y])
        if y == (len(grid) - 1):
            break
        for x in range(len(grid[0])):
            cell = "|" if SOUTH in PIPES[grid[y][x]] and NORTH in PIPES[grid[y+1][x]] else "."
            expanded.append(cell)
        new_grid_y.append(expanded)

    new_grid_x = []
    for y in range(len(new_grid_y)):
        expanded = []
        for x in range(len(new_grid_y[0])):
            expanded.append(new_grid_y[y][x])
            if x == (len(grid[0]) - 1):
                break
            cell = "-" if EAST in PIPES[new_grid_y[y][x]] and WEST in PIPES[new_grid_y[y][x+1]] else "."
            expanded.append(cell)
        new_grid_x.append(expanded)

    return new_grid_x


assert_equals(find_furthest(TEST_INPUT), 4)
assert_equals(find_furthest(TEST_INPUT_2), 4)
assert_equals(find_furthest(TEST_INPUT_3), 8)
print("Part One: ", find_furthest(INPUT))

assert_equals(find_enclosed(TEST_INPUT_4), 4)
assert_equals(find_enclosed(TEST_INPUT_5), 8)
assert_equals(find_enclosed(TEST_INPUT_6), 10)
print("Part Two: ", find_enclosed(INPUT))