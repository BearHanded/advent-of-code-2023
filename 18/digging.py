from util import christmas_input
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
TEST_INPUT_2 = 'test_input2.txt'

DIRECTIONS = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def shortest_path(f):
    commands = [(i, int(j), k) for (i, j, k) in [row.split()
                                                 for row in christmas_input.file_to_array(f)]]
    max_size = sum([command[1] for command in commands])*2
    grid = [["."]*max_size for i in range(max_size)]
    idx = (int(max_size/2), int(max_size/2))
    grid[idx[1]][idx[0]] = "#"
    print(idx, "in", max_size)
    for command in commands:
        for _ in range(command[1]):
            if command[0] in ["U", "D"]:
                grid[idx[1]][idx[0]] = command[0]

            direction = DIRECTIONS[command[0]]
            idx = (idx[0] + direction[0], idx[1] + direction[1])
            grid[idx[1]][idx[0]] = command[0]

    for y, row in enumerate(grid):
        inside_hole = False
        for x, cell in enumerate(row):
            if cell == "U":
                inside_hole = True
            elif cell == "D":
                inside_hole = False
            if cell == "." and inside_hole:
                grid[y][x] = "#"

    # for row in grid:
    #     print("".join(row))
    size = sum([len([j for j in row if j != "."]) for row in grid])
    print(size)
    return size


assert shortest_path(TEST_INPUT) == 62
print("Part One: ", shortest_path(INPUT))
