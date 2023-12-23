from util import assert_equals, file_to_array, file_as_string
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def get_hash_sum(f):
    strings = file_as_string(f).split(",")
    return sum([get_hash(string) for string in strings])


def get_hash(string):
    value = 0
    for char in string:
        value = ((value + ord(char)) * 17) % 256
    return value


def build_hash_map(f):
    commands = file_as_string(f).split(",")
    boxes = {}
    for cmd in commands:
        if "-" in cmd:
            op_idx = cmd.index("-")
            label = cmd[:op_idx]
            hash_value = get_hash(label)
            if hash_value in boxes:
                boxes[hash_value] = [i for i in boxes[hash_value] if i[0] != label]
        if "=" in cmd:
            op_idx = cmd.index("=")
            label = cmd[:op_idx]
            hash_value = get_hash(label)
            if hash_value not in boxes:
                boxes[hash_value] = []
            existing_box = next((i for i, v in enumerate(boxes[hash_value]) if v[0] == label), -1)
            if existing_box != -1:
                boxes[hash_value][existing_box] = (label, int(cmd[op_idx+1:]))
            else:
                boxes[hash_value].append((label, int(cmd[op_idx+1:])))

    # calc
    total = 0
    for box_idx, box in boxes.items():
        for lens_idx, lens in enumerate(box):
            total += (box_idx + 1) * (lens_idx + 1) * lens[1]
    return total


assert_equals(get_hash_sum(TEST_INPUT), 1320)
print("Part One: ", get_hash_sum(INPUT))

assert_equals(build_hash_map(TEST_INPUT), 145)
print("Part Two: ", build_hash_map(INPUT))