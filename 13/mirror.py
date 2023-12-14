from util import christmas_input
import numpy as np
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def part_one(f):
    patterns = np.array(christmas_input.file_to_array(f))
    groups = [[]]
    total_left = 0
    total_above = 0

    for row in patterns:
        if not len(row):
            groups.append([])
            continue
        groups[-1].append(row)
    for group in groups:
        for row in group:
            print(row)
        total_above += calc_mirrors(group)
        total_left += calc_mirrors(["".join(i) for i in list(zip(*group[::-1]))])  # clockwise
    return total_left + 100 * total_above


def calc_mirrors(group):
    for idx in range(len(group) - 1):
        size = min(idx + 1, len(group) - (idx + 1))
        if "".join(group[:idx+1][-size:]) == "".join(group[idx+1:][:size][::-1]):
            return idx + 1
    return 0


assert part_one(TEST_INPUT) == 405
print("Part One: ", part_one(INPUT))
