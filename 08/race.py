from util import christmas_input
import numpy as np

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
TEST_INPUT2 = 'test_input2.txt'
TEST_INPUT3 = 'test_input3.txt'


def desert_walk(f):
    pattern, nodes = build_nodes(f)
    curr = 'AAA'
    distance = 0
    seeking = True
    while seeking:
        direction = pattern[distance % len(pattern)]
        distance += 1
        curr = nodes[curr][0 if direction == "L" else 1]
        if curr == "ZZZ":
            seeking = False

    return distance


def ghost_walk(f):
    pattern, nodes = build_nodes(f)
    curr = [s for s in nodes.keys() if s[2] == "A"]
    print(curr)
    distance = 0
    seeking = True
    finished_paths = []
    while seeking:
        direction = pattern[distance % len(pattern)]
        dir_ordinal = 0 if direction == "L" else 1
        distance += 1
        curr = [nodes[key][dir_ordinal] for key in curr]
        for node in [s for s in curr if s[2] == "Z"]:
            finished_paths.append(distance)
            curr.remove(node)
        if len(curr) == 0:
            seeking = False
    return np.lcm.reduce(np.array(finished_paths))


def build_nodes(f):
    lines = christmas_input.file_to_array(f)
    pattern = lines[0]
    nodes = {}
    for line in lines[2:]:
        nodes[line[0:3]] = (line[7:10], line[12:15])
    return pattern, nodes


assert desert_walk(TEST_INPUT) == 2
assert desert_walk(TEST_INPUT2) == 6
print("Part One: ", desert_walk(INPUT))

assert ghost_walk(TEST_INPUT3) == 6
print("Part Two: ", ghost_walk(INPUT))
