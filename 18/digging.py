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
DIRECTION_NUM = ["R", "D", "L", "U"]


def dig_a_hole(f, translate_hex=False):
    commands = [(i, int(j), hex_to_command(k[2:-1])) for (i, j, k) in [row.split() for row in christmas_input.file_to_array(f)]]
    idx = (0, 0)
    internal, perimeter = 0, 0
    for line in commands:
        command = line[2] if translate_hex else (line[0], line[1])
        direction = DIRECTIONS[command[0]]
        new_idx = (idx[0] + command[1] * direction[0], idx[1] + command[1] * direction[1])
        internal += idx[0] * new_idx[1] - idx[1] * new_idx[0]
        perimeter += command[1]
        idx = new_idx
    return perimeter // 2 + internal // 2 + 1


def hex_to_command(hex_str):
    return DIRECTION_NUM[int(hex_str[-1])], int(hex_str[:-1], 16)


assert dig_a_hole(TEST_INPUT) == 62  # 38 outside, 24 inside
print("Part One: ", dig_a_hole(INPUT))
assert hex_to_command("70c710") == ("R", 461937)
assert dig_a_hole(TEST_INPUT, translate_hex=True) == 952408144115
print("Part Two: ", dig_a_hole(INPUT, translate_hex=True))
