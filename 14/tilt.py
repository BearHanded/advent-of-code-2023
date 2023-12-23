from util import assert_equals, file_to_array
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
TOTAL_CYCLES = 1000000000


def check_load(f):
    platform = [list(row) for row in file_to_array(f)]
    platform = rotate(platform)  # Rotate right for easy string ops
    platform = slide(platform)
    load = sum_weights(platform)
    return load


def spin_cycle(f):
    platform = [list(row) for row in file_to_array(f)]
    known_configs = {}
    for curr_cycle in range(1, TOTAL_CYCLES+1):
        for _ in range(4):
            platform = rotate(platform)
            platform = slide(platform)
        key = "".join(["".join(row) for row in platform])
        if key in known_configs:
            print("Loop from", known_configs[key], "to", curr_cycle)
            break
        known_configs[key] = curr_cycle

    remaining_cycles = (TOTAL_CYCLES - known_configs[key]) % (curr_cycle - known_configs[key])

    for curr_cycle in range(remaining_cycles):
        for _ in range(4):
            platform = rotate(platform)
            platform = slide(platform)

    platform = rotate(platform)  # Point North right for sums
    return sum_weights(platform)


def slide(platform):
    for row in platform:
        barrier = len(row)
        for idx in reversed(range(len(row))):
            if row[idx] == "#":
                barrier = idx
            elif row[idx] == "O":
                sub_idx = "".join(row[idx:barrier]).rfind(".")
                if sub_idx == -1:
                    continue
                row[sub_idx+idx] = "O"
                row[idx] = "."
    return platform


def rotate(platform):
    return [list(i) for i in list(zip(*platform[::-1]))]


def sum_weights(platform):
    return sum([sum([idx + 1 for idx, char in enumerate(row) if char == "O"]) for row in platform])


assert_equals(check_load(TEST_INPUT), 136)
print("Part One: ", check_load(INPUT))

assert_equals(spin_cycle(TEST_INPUT), 64)
print("Part Two: ", spin_cycle(INPUT))
