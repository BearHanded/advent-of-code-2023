import heapq
from util import christmas_input
import numpy as np
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def avail_plots(lines, max_steps, start=None):
    grid = [[c for c in row] for row in lines]
    if start == None:
        (y, x) = np.argwhere(np.array(grid) == "S").tolist()[0]
    else:
        (y, x) = start

    visited = {}
    queue = [(0, (x, y))]
    while len(queue) > 0:
        (steps, curr_idx) = heapq.heappop(queue)

        next_moves = get_next(curr_idx, steps, grid, visited, max_steps) 
        for move in next_moves:
            heapq.heappush(queue, move)
    even = len([v for v in visited.values() if v % 2 == 0])
    odd = len(visited.values()) - even
    return even, odd


def avail_plots_scaled(lines, max_steps):
    grid = [[c for c in row] for row in lines]
    (mid, _) = np.argwhere(np.array(grid) == "S").tolist()[0]
    boards = max_steps // len(grid)

    _, state_1 = avail_plots(lines, mid)               # first edge
    state_2, _ = avail_plots(lines, len(grid) + mid)   # next edge
    _, state_3 = avail_plots(lines, 2*len(grid) + mid) # next edge
    
    b0 = state_1
    b1 = state_2 - state_1 
    b2 = state_3 - state_2
    return (boards*(boards-1)//2)*(b2-b1) + b1*boards + b0

def get_next(curr_idx, steps, grid, visited, max_steps):
    if steps >= max_steps:
        return []
    next_moves = []
    next_steps = steps + 1
    for move in DIRECTIONS:
        next_idx = (curr_idx[0] + move[0], curr_idx[1] + move[1])
        if (
            grid[next_idx[1]%len(grid)][next_idx[0]%len(grid)] == "#"
            or next_idx in visited
        ):
            continue
        visited[next_idx] = next_steps  # Track being at the index
        next_moves.append((next_steps, next_idx))
    return next_moves

print("Part Two: ", avail_plots_scaled(christmas_input.file_to_array(INPUT), 26501365))
