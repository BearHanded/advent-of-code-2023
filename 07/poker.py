from functools import cmp_to_key
from util import assert_equals, file_to_array

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'

SCORE_ORDER = ["HIGH", "ONE_PAIR", "TWO_PAIR", "THREE_KIND", "FULL", "FOUR_KIND", "FIVE_KIND"]
CARD_ORDER = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


def play_poker(f):
    score = 0
    lines = [line.split(" ") for line in file_to_array(f)]
    hands = [[parts[0], int(parts[1]), score_hand(parts[0])] for parts in lines]
    hands.sort(key=cmp_to_key(compare_hands))
    print(hands)

    for idx, hand in enumerate(hands):
        score += (idx + 1) * hand[1]
    return score


def score_hand(cards):
    counts = {}
    for s in cards:
        if s in counts:
            counts[s] += 1
        else:
            counts[s] = 1
    sums = list(counts.values())
    if 5 in sums:
        return "FIVE_KIND"
    elif 4 in sums:
        return "FOUR_KIND"
    elif 3 in sums and 2 in sums:
        return "FULL"
    elif 3 in sums:
        return "THREE_KIND"
    elif sums.count(2) == 2:
        return "TWO_PAIR"
    elif 2 in sums:
        return "ONE_PAIR"
    return "HIGH"


def compare_hands(hand_a, hand_b):
    if SCORE_ORDER.index(hand_a[2]) < SCORE_ORDER.index(hand_b[2]):
        return -1
    elif SCORE_ORDER.index(hand_a[2]) > SCORE_ORDER.index(hand_b[2]):
        return 1

    for card_a, card_b in zip(hand_a[0], hand_b[0]):
        if CARD_ORDER.index(card_a) < CARD_ORDER.index(card_b):
            return -1
        elif CARD_ORDER.index(card_a) > CARD_ORDER.index(card_b):
            return 1
    return 0


assert_equals(play_poker(TEST_INPUT), 6440)
print("Part One: ", play_poker(INPUT))

