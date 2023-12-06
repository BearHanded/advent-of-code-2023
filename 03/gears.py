from util import christmas_input
import re
import numpy as np
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def number_sum(filename):
    lines = christmas_input.file_to_array(filename)
    symbols = build_symbols(lines)
    numbers = build_numbers(lines)

    sum = 0
    for symbol in symbols:
        rows, cols = symbol["adjacent"].shape
        dt = {'names': ['f{}'.format(i) for i in range(cols)],
              'formats': cols * [symbol["adjacent"].dtype]}

        for number in numbers:
            # I dug myself in a numpy hole, intersect not working with tuples otherwise
            intersection = np.intersect1d(symbol["adjacent"].view(dt), number["coords"].view(dt))
            if not number["marked"] and len(intersection) > 0:
                number["marked"] = True
                sum += number["value"]

    return sum


def build_symbols(lines):
    symbols = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if not char.isdigit() and char != ".":
                dirs = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
                adj = np.array([[x1 + x, y1 + y] for (x1, y1) in dirs])
                symbols.append({"character": char, "x": x, "y": y, "adjacent": adj})
    return symbols


def build_numbers(lines):
    numbers = []
    for y, line in enumerate(lines):
        matches = re.finditer(r'\d+', line)
        for m in matches:
            coords = np.array([[x, y] for x in range(m.start(), m.end())])
            numbers.append({"value": int(m.group()), "marked": False, "coords": coords})
    return numbers


def gear_ratio(filename):
    lines = christmas_input.file_to_array(filename)
    symbols = build_symbols(lines)
    numbers = build_numbers(lines)

    sum = 0
    for symbol in symbols:
        if symbol["character"] != "*":
            continue
        ratio = 1
        matches = 0
        rows, cols = symbol["adjacent"].shape
        dt = {'names': ['f{}'.format(i) for i in range(cols)],
              'formats': cols * [symbol["adjacent"].dtype]}

        for number in numbers:
            # I dug myself in a numpy hole, intersect not working with tuples otherwise
            intersection = np.intersect1d(symbol["adjacent"].view(dt), number["coords"].view(dt))
            if len(intersection) > 0 and matches <= 3:
                ratio *= number["value"]
                matches += 1

        if matches != 2:
            continue
        sum += ratio

    return sum


assert number_sum(TEST_INPUT) == 4361
# print("Part One: ", number_sum(INPUT))


assert gear_ratio(TEST_INPUT) == 467835
print("Part Two: ", gear_ratio(INPUT))
