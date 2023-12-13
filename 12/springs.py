from functools import lru_cache

from util import christmas_input
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def total_arrangements(f, expand=False):
    sets = [[parts[0], (int(i) for i in parts[1].split(","))] for parts in [line.split() for line in christmas_input.file_to_array(f)]]
    total = 0
    idx = 0
    for puzzle, cells in sets:
        idx += 1
        print("\nPUZZLE:", idx, puzzle)

        chunks = [i for i in puzzle.split(".") if i]
        possibilities = []
        for chunk in chunks:
            possibilities.append(possible_solutions(chunk, max(cells)))

        puzzle_options = process_possibilities(possibilities, stringify(cells), "")
        total += puzzle_options
    return total


@cache
def possible_solutions(chunk, max_size):
    if "?" not in chunk:
        result = [len(i) for i in chunk.split(".") if i]
        if all(i <= max_size for i in result):
            return [result]
        return []
    solutions = []
    solutions += possible_solutions(chunk.replace("?", "#", 1), max_size)
    solutions += possible_solutions(chunk.replace("?", ".", 1), max_size)
    return solutions


def process_possibilities(possibilities, cells, running):
    if running not in cells:
        return 0
    if len(possibilities) == 0:
        return 1 if cells == running else 0

    solutions = 0
    node = possibilities[0]
    for option in node:
        if len(option) == 0:
            solutions += process_possibilities(possibilities[1:], cells, running)
            continue
        new_running = running
        if new_running:
            new_running += ","
        new_running += stringify(option)
        solutions += process_possibilities(possibilities[1:], cells, new_running)
    return solutions


def stringify(int_array):
    return ",".join([str(i) for i in int_array])


# def unfold_arrangements(f):
#     sets = [line.split() for line in christmas_input.file_to_array(f)]
#     total = 0
#     idx = 0
#     for puzzle, cells in sets:
#         expanded_puzzle, expanded_cells = puzzle, cells
#         for i in range(4):
#             expanded_puzzle += "?" + puzzle
#             expanded_cells += "," + cells
#         idx += 1
#         print("\nPUZZLE:", idx, expanded_puzzle)
#
#         chunks = [i for i in expanded_puzzle.split(".") if i]
#         possibilities = []
#         for chunk in chunks:
#             possibilities.append(possible_solutions(chunk, max( [int(i) for i in cells.split(",")])))
#
#         puzzle_options = process_possibilities(possibilities, stringify(expanded_cells), "")
#         print("  ", puzzle_options)
#         total += puzzle_options
#     return total
#

assert total_arrangements(TEST_INPUT) == 21
# print("Part One: ", total_arrangements(INPUT))

# assert unfold_arrangements(TEST_INPUT) == 525152
