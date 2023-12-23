import heapq
from util import assert_equals, file_to_array
import numpy as np

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def avail_plots(lines, max_steps, start=None, allow_overflow=True):
    grid = [[c for c in row] for row in lines]
    if start is None:
        (y, x) = np.argwhere(np.array(grid) == "S").tolist()[0]
    else:
        (y, x) = start

    visited = {}
    queue = [(0, (x, y))]
    while len(queue) > 0:
        (steps, curr_idx) = heapq.heappop(queue)

        next_moves = get_next(curr_idx, steps, grid, visited, max_steps, allow_overflow)
        for move in next_moves:
            heapq.heappush(queue, move)
    even = len([v for v in visited.values() if v % 2 == 0])
    odd = len(visited.values()) - even
    return even, odd


def avail_plots_scaled(lines, max_steps):
    grid = [[c for c in row] for row in lines]
    boards = max_steps // len(grid)  # Number of cells from the origin on the axis
    remainder = max_steps % len(grid)

    # Board types:
    full_even, full_odd = avail_plots(lines, max_steps, allow_overflow=False)  # Flood the board
    inner_partial_even, inner_partial_odd = avail_plots(lines, remainder, allow_overflow=False)  # center up to 65
    outer_corners_even = full_even - inner_partial_even
    outer_corners_odd = full_odd - inner_partial_odd

    total = (
        ((boards+1)**2) * full_odd
        + (boards**2) * full_even
        - (boards + 1) * outer_corners_odd
        + boards * outer_corners_even
    )
    print(full_even, full_odd)
    return total


def get_next(curr_idx, steps, grid, visited, max_steps, allow_overflow):
    if steps >= max_steps:
        return []
    next_moves = []
    next_steps = steps + 1
    for move in DIRECTIONS:
        next_idx = (curr_idx[0] + move[0], curr_idx[1] + move[1])
        if (
                (not allow_overflow and not (0 <= next_idx[0] < len(grid[0]) and 0 <= next_idx[1] < len(grid)))
                or grid[next_idx[1] % len(grid)][next_idx[0] % len(grid)] == "#"
                or next_idx in visited
        ):
            continue
        visited[next_idx] = next_steps  # Track being at the index
        next_moves.append((next_steps, next_idx))
    return next_moves


print("Part Two: ", avail_plots_scaled(file_to_array(INPUT), 26501365))
