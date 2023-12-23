from util import assert_equals, file_to_array
import numpy as np
from itertools import combinations
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def find_shortest(f, factor):
    stars = [list(line) for line in file_to_array(f)]
    rotated = [list(row) for row in zip(*stars[::-1])]
    expanded_cols = [idx for idx, row in enumerate(stars) if "#" not in row]
    expanded_rows = [idx for idx, row in enumerate(rotated) if "#" not in row]
    galaxies = np.argwhere(np.array(stars) == "#").tolist()
    galaxy_dist = {}
    for ((y1, x1), (y2, x2)) in list(combinations(galaxies, 2)):
        expansion = len([row for row in expanded_rows if (x1 < row < x2) or (x2 < row < x1)]) \
                    + len([col for col in expanded_cols if (y1 < col < y2) or (y2 < col < y1)])
        galaxy_dist[(x1, y1), (x2, y2)] = abs(x1 - x2) + abs(y1 - y2) + factor * expansion - expansion
    return sum(galaxy_dist.values())


assert_equals(find_shortest(TEST_INPUT, 2), 374)
assert_equals(find_shortest(TEST_INPUT, 10), 1030)
assert_equals(find_shortest(TEST_INPUT, 100), 8410)
print("Part One: ", find_shortest(INPUT, 2))
print("Part Two: ", find_shortest(INPUT, 1000000))
