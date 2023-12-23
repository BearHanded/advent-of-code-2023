from queue import PriorityQueue
import time
from util import assert_equals, file_to_array

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
SLOPES = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}
START = (1, 0)


def walk(grid):
    visited = {}
    queue = PriorityQueue()
    queue.put((0, START, {START}))
    end = (len(grid[0]) - 2, len(grid) - 1)

    while not queue.empty():
        (steps, curr_idx, path) = queue.get()
        next_moves = get_next(curr_idx, steps, grid, visited, path)
        for move in next_moves:
            queue.put(move)
    return visited[end]


def get_next(curr_idx, steps, grid, visited, path):
    if curr_idx == (len(grid[0]) - 2, len(grid) - 1):
        return []
    next_moves = []
    curr_tile = grid[curr_idx[1]][curr_idx[0]]
    move_set = [SLOPES[curr_tile]] if curr_tile in SLOPES else DIRECTIONS

    for move in move_set:
        next_idx = (curr_idx[0] + move[0], curr_idx[1] + move[1])
        next_steps = steps + 1
        if (
            not (0 <= next_idx[0] < len(grid[0]) and 0 <= next_idx[1] < len(grid))
            or grid[next_idx[1]][next_idx[0]] == "#"
            or next_idx in path
        ):
            continue

        next_path = path.copy()
        next_path.add(next_idx)
        visited[next_idx] = next_steps
        next_moves.append((next_steps, next_idx, next_path))

    return next_moves


assert_equals(walk(file_to_array(TEST_INPUT)), 94)


start = time.time()
print("Part One: ", walk(file_to_array(INPUT)))
print(time.time() - start)