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
    ".": None,              # No Pipe
    "S": None               # Start, special handling
}


def find_furthest(f):
    grid = [[i for i in list(line)] for line in christmas_input.file_to_array(f)]
    (y, x) = np.argwhere(np.array(grid) == "S").tolist()[0]
    distance = 0
    curr_direction = pick_initial_direction(grid, x, y)
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


def pick_initial_direction(grid, start_x, start_y):
    for direction, in [NORTH, SOUTH, EAST, WEST]:
        (x, y) = directions[direction]
        pipe = get_pipe(grid, start_x + x, start_y + y)
        if pipe is None or pipe == ".":
            continue
        if direction == NORTH and SOUTH in pipes[pipe]:
            return direction
        elif direction == SOUTH and NORTH in pipes[pipe]:
            return direction
        elif direction == EAST and WEST in pipes[pipe]:
            return direction
        elif direction == WEST and EAST in pipes[pipe]:
            return direction
    return


def get_pipe(grid, x, y):
    if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
        return grid[y][x]
    return None


def find_enclosed(f):
    grid = [[i for i in list(line)] for line in christmas_input.file_to_array(f)]
    (y, x) = np.argwhere(np.array(grid) == "S").tolist()[0]
    distance = 0
    connected = set()
    curr_direction = pick_initial_direction(grid, x, y)
    curr_pipe = ""
    while curr_pipe != "S":
        x1, y1 = directions[curr_direction]
        x, y = x + x1, y + y1
        distance += 1
        curr_pipe = get_pipe(grid, x, y)
        connected.add((x, y))
        if curr_pipe == "S":
            break
        curr_direction = pipes[curr_pipe][0] if pipes[curr_pipe][1] == inverted_directions[curr_direction] \
            else pipes[curr_pipe][1]

    # print(connected)
    #     # empty = get_outer(grid, connected)
    #     # print(sorted(empty))
    #     # print(len(grid) * len(grid[0]), "-", len(empty), "-", len(connected))
    #     # # connected correct
    #     # # empty 69, should say 53
    #     # surrounded = len(grid) * len(grid[0]) - len(empty) - len(connected)
    #     # print(surrounded)
    #     #
    #     # print(sorted(empty))
    #     # empty = sorted(empty)
    #     # t = [["I"] * len(grid[0]) for i in range(len(grid))]
    #     # for x_0, y_0 in empty:
    #     #     t[y_0][x_0] = "O"
    #     # for x_0, y_0 in connected:
    #     #     t[y_0][x_0] = " "
    #     # for line in t:
    #     #     print(line)

    new_grid = expand(grid)
    return 0


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
    for y in range(len(grid)-1):
        expanded = []
        new_grid_y.append(grid[y])
        for x in range(len(grid)-1):
            cell = "|" if SOUTH in pipes[grid[y][x]] and NORTH in pipes[grid[y+1][x]] else "."
            expanded.append(cell)
        new_grid_y.append(expanded)

    print(new_grid_y)
    return new_grid_y


assert find_furthest(TEST_INPUT) == 4
assert find_furthest(TEST_INPUT_2) == 4
assert find_furthest(TEST_INPUT_3) == 8
print("Part One: ", find_furthest(INPUT))

assert find_enclosed(TEST_INPUT_4) == 4
assert find_enclosed(TEST_INPUT_5) == 8
assert find_enclosed(TEST_INPUT_6) == 10
print("Part Two: ", find_enclosed(INPUT))
