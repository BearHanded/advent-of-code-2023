from util import assert_equals, file_to_array

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
TEST_INPUT_WORDS = 'test_input_words.txt'
DIGIT_MAP = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def calibrate(filename):
    lines = file_to_array(filename)
    value = 0
    for line in lines:
        nums = [int(i) for i in list(line) if i.isdigit()]
        value += int(str(nums[0]) + str(nums[-1]))
    return value


def digitize_calibrate(filename):
    # xtwone3four makes things weird
    lines = file_to_array(filename)
    value = 0
    for line in lines:
        lowest_idx = 1000
        lowest_val = 0
        highest_idx = -1
        highest_val = 0

        # find first and last digit
        for i, c in enumerate(line):
            if c.isdigit():
                if i < lowest_idx:
                    lowest_idx = i
                    lowest_val = c
                if i > highest_idx:
                    highest_idx = i
                    highest_val = c

        # find first and last substring
        for key in DIGIT_MAP:
            low_idx = line.find(key)
            high_idx = line.rfind(key)
            if low_idx != -1 and low_idx < lowest_idx:
                lowest_idx = low_idx
                lowest_val = DIGIT_MAP[key]
            if high_idx != -1 and high_idx > highest_idx:
                highest_idx = high_idx
                highest_val = DIGIT_MAP[key]

        value += int(str(lowest_val) + str(highest_val))
    return value


assert_equals(calibrate(TEST_INPUT), 142)
print("Part One: ", calibrate(INPUT))
assert_equals(calibrate(TEST_INPUT), 142)
print("Part One: ", calibrate(INPUT))
print(digitize_calibrate(TEST_INPUT_WORDS))
assert_equals(digitize_calibrate(TEST_INPUT_WORDS), 281)
print("Part Two: ", digitize_calibrate(INPUT))
