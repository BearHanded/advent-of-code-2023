import heapq
from util import assert_equals, file_to_array
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
TEST_INPUT_2 = 'test_input2.txt'
MAX_STRAIGHT = 3
ULTRA_MIN = 4
ULTRA_MAX = 10


def shortest_path(f, ultra=False):
    grid = [[int(i) for i in row] for row in file_to_array(f)]
    visited = {}  # {(coords, direction, dist): heat}
    queue = [(0, (0, 0), (0, 1), 0), (0, (0, 0), (1, 0), 0)]  # (heat, coords, direction, dist)

    while len(queue) > 0:
        (heat, curr_idx, direction, straight_distance) = heapq.heappop(queue)
        next_moves = get_next(curr_idx, direction, straight_distance, heat, grid, visited, ultra)
        for move in next_moves:
            heapq.heappush(queue, move)
        result = next((move for move in next_moves if move[1] == (len(grid[0])-1, len(grid)-1)), False)
        if result and (not ultra or result[3] >= ULTRA_MIN):
            return result[0]


def get_next(curr_idx, curr_dir, straight_distance, heat, grid, visited, ultra):
    """Returns a list of possible moves as [(heat, (x,y), (dir_x, dir_y), straight_distance)]"""
    avail = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    avail.remove((curr_dir[0] * -1, curr_dir[1] * -1))  # can't go backwards
    next_moves = []
    for move in avail:
        next_idx = (curr_idx[0] + move[0], curr_idx[1] + move[1])
        if (
                not (0 <= next_idx[0] < len(grid[0]) and 0 <= next_idx[1] < len(grid))       # outside grid dimensions
                or (not ultra and (curr_dir == move and straight_distance >= MAX_STRAIGHT))  # standard: too far, turn
                or (ultra and ((curr_dir == move and straight_distance >= ULTRA_MAX)         # ultra: too far, turn
                    or (curr_dir != move and straight_distance < ULTRA_MIN)))                # ultra: not far enough
        ):
            continue
        next_heat = heat + grid[next_idx[1]][next_idx[0]]
        next_dist = straight_distance + 1 if curr_dir == move else 1
        if (next_idx, move, next_dist) not in visited:
            visited[(next_idx, move, next_dist)] = next_heat
            next_moves.append((next_heat, next_idx, move, next_dist))
    return next_moves


assert_equals(shortest_path(TEST_INPUT), 102)
print("Part One: ", shortest_path(INPUT))

assert_equals(shortest_path(TEST_INPUT, True), 94)
assert_equals(shortest_path(TEST_INPUT_2, True), 71)
print("Part Two: ", shortest_path(INPUT, True))
