from util import christmas_input
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def check_load(f):
    platform = [list(row) for row in christmas_input.file_to_array(f)]
    platform = rotate(platform)  # Rotate right for easy string ops
    platform = slide(platform)
    load = sum_weights(platform)
    return load


def spin_cycle(f):
    platform = [list(row) for row in christmas_input.file_to_array(f)]
    total_cycles = 1000000000
    known_configs = {}
    for curr_cycle in range(1, total_cycles+1):
        for _ in range(4):
            platform = rotate(platform)
            platform = slide(platform)
        key = "".join(["".join(row) for row in platform])
        if key in known_configs:
            print("Loop from", known_configs[key], "to", curr_cycle)
            break
        known_configs[key] = curr_cycle

    # find offset in loop for final calculation:
    cycle_length = curr_cycle - known_configs[key]
    cycle_start = known_configs[key]
    remaining_cycles = (total_cycles-cycle_start) % cycle_length

    for curr_cycle in range(remaining_cycles):
        for _ in range(4):
            platform = rotate(platform)
            platform = slide(platform)

    # Calculate
    platform = rotate(platform)
    load = sum_weights(platform)

    print(load)
    return load


def rotate(platform, amount=1):
    out = platform
    for _ in range(amount):
        out = [list(i) for i in list(zip(*out[::-1]))]
    return out


def slide(platform):
    for row in platform:
        barrier = len(row)
        for idx in reversed(range(len(row))):
            if row[idx] == "#":
                barrier = idx
            elif row[idx] == "O":
                # Slide to barrier or O
                sub_idx = "".join(row[idx:barrier]).rfind(".")
                if sub_idx == -1:
                    continue
                row[sub_idx+idx] = "O"
                row[idx] = "."
    return platform


def sum_weights(platform):
    load = 0
    for row in platform:
        for idx, char in enumerate(row):
            if char == "O":
                load += idx+1
    return load


assert check_load(TEST_INPUT) == 136
print("Part One: ", check_load(INPUT))

assert spin_cycle(TEST_INPUT) == 64
print("Part Two: ", spin_cycle(INPUT))
