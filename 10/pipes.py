from util import christmas_input
import numpy as np

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
TEST_INPUT_2 = 'test_input2.txt'
TEST_INPUT_3 = 'test_input3.txt'
TEST_INPUT_4 = 'test_input4.txt'
TEST_INPUT_5 = 'test_input5.txt'
TEST_INPUT_6 = 'test_input6.txt'


# I sure dug a hole for myself...
NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"
NORTHWEST = "NW"
NORTHEAST = "NE"
SOUTHWEST = "SW"
SOUTHEAST = "SE"
directions = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    EAST: (1, 0),
    WEST: (-1, 0),
    NORTHWEST: (-1, -1),
    NORTHEAST: (1, -1),
    SOUTHWEST: (-1, 1),
    SOUTHEAST: (1, 1),
}
inverted_directions = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
}
pipes = {
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
    grid = [[i for i in list(line)] for line in christmas_input.file_to_array(f)]
    (y, x) = np.argwhere(np.array(grid) == "S").tolist()[0]
    distance = 0
    curr_direction = pipes[find_start_piece(grid, x, y)][0]
    curr_pipe = ""
    while curr_pipe != "S":
        x1, y1 = directions[curr_direction]
        x, y = x + x1, y + y1
        distance += 1
        curr_pipe = get_pipe(grid, x, y)
        if curr_pipe == "S":
            break
        curr_direction = pipes[curr_pipe][0] if pipes[curr_pipe][1] == inverted_directions[curr_direction] \
            else pipes[curr_pipe][1]

    return int(distance/2)


def find_start_piece(grid, start_x, start_y):
    connections = []
    for direction, in [NORTH, SOUTH, EAST, WEST]:
        (x, y) = directions[direction]
        pipe = get_pipe(grid, start_x + x, start_y + y)
        if pipe is None or pipe == ".":
            continue
        if direction == NORTH and SOUTH in pipes[pipe]:
            connections.append(NORTH)
        elif direction == SOUTH and NORTH in pipes[pipe]:
            connections.append(SOUTH)
        elif direction == EAST and WEST in pipes[pipe]:
            connections.append(EAST)
        elif direction == WEST and EAST in pipes[pipe]:
            connections.append(WEST)

    for key in pipes:
        if pipes[key] is not None and connections[0] in pipes[key] and connections[1] in pipes[key]:
            return key


def get_pipe(grid, x, y):
    if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
        return grid[y][x]
    return None


def find_enclosed(f):
    original_grid = [[i for i in list(line)] for line in christmas_input.file_to_array(f)]

    (y, x) = np.argwhere(np.array(original_grid) == "S").tolist()[0]
    initial_piece = find_start_piece(original_grid, x, y)
    original_grid[y][x] = initial_piece  # Replace for later math

    y *= 2  # prep for expansion ?????????????
    x *= 2

    (initial_y, initial_x) = (y, x)
    curr_direction = pipes[initial_piece][0]
    curr_pipe = ""
    grid = expand(original_grid)

    connected = set()
    while True:
        x1, y1 = directions[curr_direction]
        x, y = x + x1, y + y1
        curr_pipe = get_pipe(grid, x, y)
        connected.add((x, y))
        if x == initial_x and y == initial_y:
            break
        curr_direction = pipes[curr_pipe][0] if pipes[curr_pipe][1] == inverted_directions[curr_direction] \
            else pipes[curr_pipe][1]

    empty = get_outer(grid, connected)
    reduced_empty = list(filter(lambda pair: pair[0] % 2 == 0 and pair[1] % 2 == 0, empty))
    reduced_connected = list(filter(lambda pair: pair[0] % 2 == 0 and pair[1] % 2 == 0, connected))
    surrounded = len(original_grid) * len(original_grid[0]) - len(reduced_empty) - len(reduced_connected)

    t = [["I"] * len(original_grid[0]) for i in range(len(original_grid))]
    for x_0, y_0 in reduced_empty:
        t[int(y_0/2)][int(x_0/2)] = "O"
    for x_0, y_0 in reduced_connected:
        t[int(y_0/2)][int(x_0/2)] = " "
    for line in t:
        print(line)
    return surrounded


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

    growing = True
    while growing:
        next_empty = empty.copy()

        for (x, y) in empty:
            for x1, y1 in directions.values():
                new_x = x + x1
                new_y = y + y1
                if 0 < new_x < max_x and 0 < new_y < max_y and (new_x, new_y) not in connected:
                    next_empty.add((new_x, new_y))
        if len(next_empty) == len(empty):
            growing = False
        empty = next_empty
    return empty


def expand(grid):
    new_grid_y = []
    for y in range(len(grid)):
        expanded = []
        new_grid_y.append(grid[y])
        if y == (len(grid) - 1):
            break
        for x in range(len(grid[0])):
            cell = "|" if SOUTH in pipes[grid[y][x]] and NORTH in pipes[grid[y+1][x]] else "."
            expanded.append(cell)
        new_grid_y.append(expanded)

    new_grid_x = []
    for y in range(len(new_grid_y)):
        expanded = []
        for x in range(len(new_grid_y[0])):
            expanded.append(new_grid_y[y][x])
            if x == (len(grid[0]) - 1):
                break
            cell = "-" if EAST in pipes[new_grid_y[y][x]] and WEST in pipes[new_grid_y[y][x+1]] else "."
            expanded.append(cell)
        new_grid_x.append(expanded)

    return new_grid_x


assert find_furthest(TEST_INPUT) == 4
assert find_furthest(TEST_INPUT_2) == 4
assert find_furthest(TEST_INPUT_3) == 8
print("Part One: ", find_furthest(INPUT))

assert find_enclosed(TEST_INPUT_4) == 4
assert find_enclosed(TEST_INPUT_5) == 8
assert find_enclosed(TEST_INPUT_6) == 10
print("Part Two: ", find_enclosed(INPUT))
