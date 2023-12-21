import heapq
from operator import add
from util import christmas_input
import numpy as np
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def avail_plots(f, max_steps):
    grid = [[c for c in row] for row in christmas_input.file_to_array(f)]
    (y, x) = np.argwhere(np.array(grid) == "S").tolist()[0]
    visited = {}
    queue = [(0, (x, y))]
    while len(queue) > 0:
        (steps, curr_idx) = heapq.heappop(queue)

        next_moves = get_next(curr_idx, steps, grid, visited, max_steps) 
        for move in next_moves:
            heapq.heappush(queue, move)
            
    return len([v for v in visited.values() if v % 2 == 0])

def get_next(curr_idx, steps, grid, visited, max_steps):
    if steps >= max_steps:
        return []
    next_moves = []
    next_steps = steps + 1
    for move in DIRECTIONS:
        next_idx = (curr_idx[0] + move[0], curr_idx[1] + move[1])
        if (
            not (0 <= next_idx[0] < len(grid[0]) and 0 <= next_idx[1] < len(grid))
            or grid[next_idx[1]][next_idx[0]] == "#"
            or next_idx in visited
        ):
            continue
        visited[next_idx] = next_steps  # Track being at the index
        next_moves.append((next_steps, next_idx))
    return next_moves

assert avail_plots(TEST_INPUT, 6) == 16
print("Part One: ", avail_plots(INPUT, 64))
