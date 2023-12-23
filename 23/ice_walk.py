import heapq
import time
from util import assert_equals, file_to_array
import re

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
SLOPES = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}


def part_one(f):
    lines = file_to_array(f)
    paths = walk((1, 0), lines, set())
    return max(paths) - 1


def walk(curr_idx, grid, path):
    # TODO: track current path, don't backtrack
    # TODO: Note the input has dead ends
    path.add(curr_idx)
    if curr_idx == (len(grid[0]) - 2, len(grid) - 1):
        return [len(path)]
    options = []
    for move in DIRECTIONS:
        new_path = path.copy()
        next_idx = (curr_idx[0] + move[0], curr_idx[1] + move[1])
        if (
            not (0 <= next_idx[0] < len(grid[0]) and 0 <= next_idx[1] < len(grid))
            or grid[next_idx[1]][next_idx[0]] == "#"
            or next_idx in new_path
        ):
            continue

        # ICE SLOPE
        next_tile = grid[next_idx[1]][next_idx[0]]
        if next_tile in SLOPES.keys():
            if SLOPES[next_tile] == (move[0] * -1, move[1] * -1):  # Can't go up a slope
                continue
            new_path.add(next_idx)
            next_idx = (curr_idx[0] + SLOPES[next_tile][0], curr_idx[1] + SLOPES[next_tile][1])  # SLIDE FORWARD
        options += walk(next_idx, grid, new_path)
        # print(options)
    return options


assert_equals(part_one(TEST_INPUT), 94)
start = time.time()
print("Part One: ", part_one(INPUT))
end = time.time()
print(end - start)
