from util import christmas_input
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
MAX_STRAIGHT = 3


def shortest_path(f, ultra=False):
    grid = [[int(i) for i in row] for row in christmas_input.file_to_array(f)]
    destination = (len(grid[0])-1, len(grid)-1)
    print("Seeking", destination)
    initial_state = ((0, 0), (0, 1), 0, 0)  # coordinates, direction, remaining before turn, heat
    queue = [initial_state]
    visited = {}  # coordinates, direction, remaining before turn: heat

    while len(queue) > 0:
        next_item = min([(heat, i) for i, (_, _, _, heat) in enumerate(queue)])
        (curr_idx, direction, straight_distance, heat) = queue.pop(next_item[1])
        next_moves = get_next(curr_idx, direction, straight_distance, heat, grid, visited)
        queue = queue + next_moves

        finished = next((move for move in next_moves if move[0] == destination), False)
        if finished:
            return finished[3]

    return min([h for (idx, _, _), h in visited.items() if idx == destination])


def get_next(curr_idx, curr_dir, straight_distance, heat, grid, visited):
    """Returns a tuple of possible moves ((x,y), (dir_x, dir_y), straight_distance, heat)"""
    avail = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    avail.remove((curr_dir[0] * -1, curr_dir[1] * -1))  # can't go backwards
    next_moves = []
    for move in avail:
        next_idx = (curr_idx[0] + move[0], curr_idx[1] + move[1])
        if not (0 <= next_idx[0] < len(grid[0]) and 0 <= next_idx[1] < len(grid)) \
                or (curr_dir == move and straight_distance >= MAX_STRAIGHT):
            continue
        next_heat = heat + grid[next_idx[1]][next_idx[0]]
        next_dist = straight_distance + 1 if curr_dir == move else 1
        next_move = (next_idx, move, next_dist, next_heat)
        next_move_key = (next_idx, move, next_dist)
        if next_move_key not in visited or next_heat < visited[next_move_key]:
            visited[next_move_key] = next_heat
            next_moves.append(next_move)
    return next_moves


assert shortest_path(TEST_INPUT) == 102
print("Part One: ", shortest_path(INPUT))

assert shortest_path(TEST_INPUT, True) == 71
print("Part Two: ", shortest_path(INPUT, True))
