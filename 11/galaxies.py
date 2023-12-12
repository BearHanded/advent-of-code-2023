from util import christmas_input
import numpy as np
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def find_shortest(f, expansion_size):
    stars = [list(line) for line in christmas_input.file_to_array(f)]
    rotated = [list(row) for row in zip(*stars[::-1])]
    expanded_cols = [idx for idx, row in enumerate(stars) if "#" not in row]
    expanded_rows = [idx for idx, row in enumerate(rotated) if "#" not in row]

    galaxies = np.argwhere(np.array(stars) == "#").tolist()
    galaxy_dist = {}
    for i, galaxy in enumerate(galaxies):
        y1, x1 = galaxy
        for galaxy2 in galaxies[i+1:]:
            y2, x2 = galaxy2
            match_x = [row for row in expanded_rows if (x1 < row < x2) or (x2 < row < x1)]
            match_y = [col for col in expanded_cols if (y1 < col < y2) or (y2 < col < y1)]
            expanded_space = expansion_size * (len(match_x) + len(match_y)) - (len(match_x) + len(match_y))
            galaxy_dist[(x1, y1), (x2, y2)] = abs(x1 - x2) + abs(y1 - y2) + expanded_space
    return sum(galaxy_dist.values())


assert find_shortest(TEST_INPUT, 2) == 374
assert find_shortest(TEST_INPUT, 10) == 1030
assert find_shortest(TEST_INPUT, 100) == 8410
print("Part One: ", find_shortest(INPUT, 2))
print("Part Two: ", find_shortest(INPUT, 1000000))
