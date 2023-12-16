from util import christmas_input
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def calc_tiles(grid, start=(0, 0), direction=(1, 0)):
    rays = {}  # (start, dir) : (end)
    tiles = set()
    ray_trace((start[0] - direction[0], start[1] - direction[1]), direction, grid, rays, tiles)  # Start entering 0,0
    return len(tiles)


def max_tiles(f):
    grid = christmas_input.file_to_array(f)
    sums = []
    for y in range(len(grid)):
        sums.append(calc_tiles(grid, (0, y), (1, 0)))
        sums.append(calc_tiles(grid, (len(grid[0]), y), (-1, 0)))
    for x in range(len(grid[0])):
        sums.append(calc_tiles(grid, (x, 0), (0, 1)))
        sums.append(calc_tiles(grid, (x, len(grid)), (0, -1)))
    return max(sums)


def ray_trace(start, direction, grid, rays, tiles):
    if (start, direction) in rays:
        return
    idx = start
    while True:
        idx = (idx[0] + direction[0], idx[1] + direction[1])
        if idx[0] < 0 or idx[0] >= len(grid[0]) or idx[1] < 0 or idx[1] >= len(grid):
            return
        tiles.add(idx)
        if grid[idx[1]][idx[0]] == "|" and direction in [(1, 0), (-1, 0)]:
            rays[(start, direction)] = idx
            ray_trace(idx, (0, 1), grid, rays, tiles)
            ray_trace(idx, (0, -1), grid, rays, tiles)
            return
        if grid[idx[1]][idx[0]] == "-" and direction in [(0, 1), (0, -1)]:
            rays[(start, direction)] = idx
            ray_trace(idx, (1, 0), grid, rays, tiles)
            ray_trace(idx, (-1, 0), grid, rays, tiles)
            return
        if grid[idx[1]][idx[0]] == "/":
            rays[(start, direction)] = idx
            new_dir = (-1 * direction[1], -1 * direction[0])
            ray_trace(idx, new_dir, grid, rays, tiles)
            return
        if grid[idx[1]][idx[0]] == "\\":
            rays[(start, direction)] = idx
            new_dir = (direction[1], direction[0])
            ray_trace(idx, new_dir, grid, rays, tiles)
            return


assert calc_tiles(christmas_input.file_to_array(TEST_INPUT)) == 46
print("Part One: ", calc_tiles(christmas_input.file_to_array(INPUT)))
assert max_tiles(TEST_INPUT) == 51
print("Part Two: ", max_tiles(INPUT))

