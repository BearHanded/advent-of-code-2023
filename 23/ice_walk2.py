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
    end = (len(grid[0]) - 2, len(grid) - 1)

    intersections = build_intersections(grid, end)
    network = connect_graph(intersections, grid)
    visited = dict([(i, 0) for i in intersections.keys()])

    queue = PriorityQueue()
    queue.put((0, START, {START}))
    while not queue.empty():
        (steps, curr_idx, path) = queue.get()
        next_moves = get_next(curr_idx, steps, network, visited, path, end)
        for move in next_moves:
            queue.put(move)
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
                connections.append((next_idx, len(path)))  # Don't count the source intersection
        graph[intersection] = connections
    return graph


def get_next(curr_idx, steps, graph, visited, path, end):
    if curr_idx == end:
        return []
    next_moves = []

    for neighbor, cost in graph[curr_idx]:
        next_steps = steps + cost
        if neighbor in path:
            continue

        next_path = path.copy()
        next_path.add(neighbor)
        visited[neighbor] = max(visited[neighbor], next_steps)
        next_moves.append((next_steps, neighbor, next_path))
    return next_moves


assert_equals(len(build_intersections(file_to_array(TEST_INPUT), (21, 22))), 9)
assert_equals(walk(file_to_array(TEST_INPUT)), 154)


start = time.time()
print("Part Two: ", walk(file_to_array(INPUT)))
print(time.time() - start)