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


def walk(grid, slippery=True):
    print(len(grid[0]), "x", len(grid))
    visited = {}
    queue = PriorityQueue()
    queue.put((0, START, {START}))
    end = (len(grid[0]) - 2, len(grid) - 1)

    intersections = build_intersections(grid, end)
    network = connect_graph(intersections, grid)

    while not queue.empty():
        (steps, curr_idx, path) = queue.get()
        next_moves = get_next(curr_idx, steps, grid, visited, path, slippery)
        for move in next_moves:
            queue.put(move)
    print(visited[end])
    return visited[end]


def build_intersections(grid, end):
    intersections = {}
    for y, line in enumerate(grid):
        for x, char in enumerate(list(line)):
            if char == "#":
                continue
            neighbors = []
            for direction in DIRECTIONS:  # Build neighbors for a node, we'll chase these down next
                next_idx = (x + direction[0], y + direction[1])
                if (
                    not (0 <= next_idx[0] < len(grid[0]) and 0 <= next_idx[1] < len(grid))
                    or grid[next_idx[1]][next_idx[0]] == "#"
                ):
                    continue
                neighbors.append(next_idx)
            if (x, y) == START or (x, y) == end or len(neighbors) > 2:  # Not a path
                intersections[(x, y)] = neighbors
    return intersections


def connect_graph(intersections, grid):
    graph = {}
    for intersection, neighbors in intersections.items():
        print("BUILDING", intersection)
        connections = []
        for neighbor in neighbors:
            path = {intersection}
            next_idx = neighbor

            while next_idx not in intersections or next_idx is None:
                curr_idx = next_idx
                path.add(curr_idx)
                next_idx = None

                for move in DIRECTIONS:
                    candidate = (curr_idx[0] + move[0], curr_idx[1] + move[1])
                    if (
                            not (0 <= candidate[0] < len(grid[0]) and 0 <= candidate[1] < len(grid)) # OOB
                            or grid[candidate[1]][candidate[0]] == "#"
                            or candidate in path  # Backwards
                    ):
                        continue
                    next_idx = candidate

            if next_idx:
                print("  - attaching", next_idx, len(path))
                connections.append((next_idx, len(path)))  # Don't count the source intersection
        graph[intersection] = connections
    return graph


def get_next(curr_idx, steps, grid, visited, path, slippery):
    if curr_idx == (len(grid[0]) - 2, len(grid) - 1):
        return []
    next_moves = []
    curr_tile = grid[curr_idx[1]][curr_idx[0]]
    move_set = [SLOPES[curr_tile]] if (slippery and curr_tile in SLOPES) else DIRECTIONS

    for move in move_set:
        next_idx = (curr_idx[0] + move[0], curr_idx[1] + move[1])
        next_steps = steps + 1
        if (
            not (0 <= next_idx[0] < len(grid[0]) and 0 <= next_idx[1] < len(grid))
            or grid[next_idx[1]][next_idx[0]] == "#"
            or next_idx in path
            # or (next_idx in visited and visited[next_idx] > steps)
        ):
            continue

        next_path = path.copy()
        next_path.add(next_idx)
        visited[next_idx] = next_steps
        next_moves.append((next_steps, next_idx, next_path))

    return next_moves


assert_equals(len(build_intersections(file_to_array(TEST_INPUT), (21, 22))), 9)
assert_equals(walk(file_to_array(TEST_INPUT)), 94)
assert_equals(walk(file_to_array(TEST_INPUT), False), 154)


start = time.time()
print("Part One: ", walk(file_to_array(INPUT)))
print(time.time() - start)

start = time.time()
print("Part Two: ", walk(file_to_array(INPUT), False))
print(time.time() - start)