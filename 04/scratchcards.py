from util import christmas_input
import numpy as np
import re

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def score_game(game_string):
    score = 0
    data = re.sub(" +", " ", game_string).split(" ")
    pivot = data.index("|")
    winning = np.array(data[2:pivot])
    playing = np.array(data[pivot:])
    matches = np.intersect1d(winning, playing)
    if len(matches):
        return 2**(len(matches)-1)
    return score


def sum_games(filename):
    lines = christmas_input.file_to_array(filename)
    return sum([score_game(line) for line in lines])


def score_game_additive(game_string):
    data = re.sub(" +", " ", game_string).split(" ")
    pivot = data.index("|")
    winning = np.array(data[2:pivot])
    playing = np.array(data[pivot:])
    matches = np.intersect1d(winning, playing)
    return len(matches)

def grow_games(filename):
    lines = christmas_input.file_to_array(filename)
    total_cards = 0
    game_lookup = [{"score": score_game_additive(line), "count": 1} for line in lines]
    for idx, game in enumerate(game_lookup):
        total_cards += game["count"]
        if game["score"] == 0:
            continue
        for cascade in game_lookup[idx+1:(idx+game["score"]+1)]:
            cascade["count"] += game["count"]

    print(game_lookup)
    print(total_cards)

    return total_cards


assert sum_games(TEST_INPUT) == 13
print("Part One: ", sum_games(INPUT))

assert grow_games(TEST_INPUT) == 30
print("Part Two: ", grow_games(INPUT))

