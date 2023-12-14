from util import christmas_input
import numpy as np
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def mirror_sum(f, clean_mirrors=False):
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
        total_above += calc_mirrors(group, clean_mirrors)
        total_left += calc_mirrors(["".join(i) for i in list(zip(*group[::-1]))], clean_mirrors)  # clockwise
    return total_left + 100 * total_above


def calc_mirrors(group, clean_mirrors):
    for idx in range(len(group) - 1):
        size = min(idx + 1, len(group) - (idx + 1))
        original = "".join(group[:idx+1][-size:])
        reflection = "".join(group[idx+1:][:size][::-1])

        if clean_mirrors and sum(1 for a, b in zip(original, reflection) if a != b) == 1:
            return idx + 1
        if not clean_mirrors and original == reflection:
            return idx + 1
    return 0


assert mirror_sum(TEST_INPUT) == 405
print("Part One: ", mirror_sum(INPUT))
assert mirror_sum(TEST_INPUT, True) == 400
print("Part Two: ", mirror_sum(INPUT, True))