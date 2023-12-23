from functools import lru_cache
from util import assert_equals, file_to_array

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def total_arrangements(f, expand=False):
    sets = [line.split() for line in file_to_array(f)]
    total = 0
    for puzzle, cells in sets:
        if expand:
            expanded_puzzle = puzzle
            expanded_cells = cells
            for i in range(4):
                expanded_puzzle += "?" + puzzle
                expanded_cells += "," + cells
            puzzle = expanded_puzzle
            cells = expanded_cells
        cells = [int(x) for x in cells.split(',')]
        total += possible_solutions(tuple(puzzle), tuple(cells))
    return total


@lru_cache()
def possible_solutions(puzzle, cells):
    solutions = 0
    if len(cells) == 0:  # reached a match
        return 1 if '#' not in puzzle else 0
    elif sum(cells) + len(cells) - 1 > len(puzzle):
        return 0
    elif puzzle[0] == '.':  # skip
        return possible_solutions(puzzle[1:], cells)
    elif puzzle[0] == '?':  # look forward + consider current match
        solutions += possible_solutions(puzzle[1:], cells)

    cell_length = cells[0]
    # current cell_length is valid for an item, look forward for next cell
    if '.' not in puzzle[:cell_length] and (len(puzzle) <= cell_length or len(puzzle) > cell_length and puzzle[cell_length] != '#'):
        solutions += possible_solutions(puzzle[cell_length + 1:], cells[1:])

    return solutions


assert_equals(total_arrangements(TEST_INPUT), 21)
assert_equals(total_arrangements(TEST_INPUT, True), 525152)
print("Part One: ", total_arrangements(INPUT))
print("Part Two: ", total_arrangements(INPUT, True))
