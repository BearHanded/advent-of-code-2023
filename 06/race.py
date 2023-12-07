from util import christmas_input
import re

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def find_solutions(races):
    count = 1
    for (time, record) in zip(races[0], races[1]):
        count *= total_solutions(time, record)
    return count


def total_solutions(time, record):
    total = 0
    for charge in range(0, time):
        if charge * (time - charge) > record:
            total += 1
    return total


def bad_kerning_races(f):
    lines = [[int(i) for i in re.sub(" +", " ", line).split(" ")[1:]] for line in christmas_input.file_to_array(f)]
    return find_solutions(lines)


def legible_races(f):
    numbers = [re.sub(" +", " ", line).split(" ")[1:] for line in christmas_input.file_to_array(f)]
    formatted = [[int("".join(i))] for i in numbers]
    return find_solutions(formatted)


assert bad_kerning_races(TEST_INPUT) == 288
print("Part One: ", bad_kerning_races(INPUT))

assert legible_races(TEST_INPUT) == 71503
print("Part Two: ", legible_races(INPUT))
