from functools import cmp_to_key
from util import christmas_input
import re

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def play_poker(f):
    score = 0
    # scores = [[(parts[0], int(parts[1])) for parts in line.split(
    #     " ")] for line in christmas_input.file_to_array(f)]
    hands = [(parts[0], int(parts[1])) for parts in [line.split(" ")
                                                     for line in christmas_input.file_to_array(f)]]
    hands.sort(key=cmp_to_key(compare_hands))
    print(hands)

    for idx, hand in enumerate(hands):
        score += (idx + 1) * hand[1]
    return score


def compare_hands(hand_a, hand_b):
    return 1
    parts = hand_string.split(" ")
    print(hand, bid)
    return 1


assert play_poker(TEST_INPUT) == 6440
print("Part One: ", play_poker(INPUT))

# assert legible_races(TEST_INPUT) == 71503
# print("Part Two: ", legible_races(INPUT))
