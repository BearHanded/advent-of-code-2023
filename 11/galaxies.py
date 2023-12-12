from util import christmas_input
import numpy as np
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def find_shortest(f, expansion_size):
    stars = [list(line) for line in christmas_input.file_to_array(f)]

    expanded = expand_y(stars)
    expanded = [list(row) for row in zip(*expanded[::-1])] # clockwise
    expanded = expand_y(expanded)
    expanded = [list(row) for row in zip(*expanded)][::-1] # anti-clockwise

    for line in expanded:
        print(line)

    galaxies = np.argwhere(np.array(expanded) == "#").tolist()
    print(galaxies)
    galaxy_dist = {}
    for i, galaxy in enumerate(galaxies):
        x1, y1 = galaxy
        for galaxy2 in galaxies[i+1:]:
            x2, y2 = galaxy2
            galaxy_dist[(x1, y1), (x2, y2)] = abs(x1 - x2) + abs(y1 - y2)

    for dist in galaxy_dist:
        print(dist, galaxy_dist[dist])
    print(sum(galaxy_dist.values()))
    return sum(galaxy_dist.values())


def expand_y(grid):
    # I already wrote this for the last problem
    new_grid = []
    for y in range(len(grid)):
        new_grid.append(grid[y])
        if "#" not in grid[y]:
            new_grid.append(grid[y].copy())
    return new_grid


assert find_shortest(TEST_INPUT, 1) == 374
print("Part One: ", find_shortest(INPUT))

assert find_shortest(TEST_INPUT, 10) == 2
assert find_shortest(TEST_INPUT, 100) == 8410
print("Part Two: ", find_shortest(INPUT, 1000000))
