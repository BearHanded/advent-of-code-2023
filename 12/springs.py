from functools import lru_cache

from util import christmas_input
import numpy as np
from itertools import combinations
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def total_arrangements(f):
    sets = [[parts[0], parts[1]] for parts in [line.split() for line in christmas_input.file_to_array(f)]]
    total = 0
    idx = 0
    for puzzle, cells in sets:
        idx += 1
        print("\nPUZZLE:", idx, puzzle)
        total += solve(puzzle, cells)
    print(total)
    return total


@lru_cache
def solve(puzzle, cells):
    puzzle.strip(".")
    if "?" not in puzzle:
        populated = ','.join([str(len(i)) for i in puzzle.split(".") if i])
        return 1 if cells == populated else 0
    solutions = 0
    solutions += solve(puzzle.replace("?", "#", 1), cells)
    solutions += solve(puzzle.replace("?", ".", 1), cells)
    return solutions


def unfold_arrangements(f):
    sets = [[parts[0], parts[1]] for parts in [line.split() for line in christmas_input.file_to_array(f)]]
    total = 0
    idx = 0
    for puzzle, cells in sets:
        expanded_puzzle, expanded_cells = puzzle, cells
        for i in range(4):
            expanded_puzzle += "?" + puzzle
            expanded_cells += "," + cells
        print(expanded_puzzle, expanded_cells)

        idx += 1
        print("\nPUZZLE:", idx, expanded_puzzle)
        total += solve(expanded_puzzle, expanded_cells)
    print(total)
    return total


assert total_arrangements(TEST_INPUT) == 21
# print("Part One: ", total_arrangements(INPUT))

assert unfold_arrangements(TEST_INPUT) == 525152
