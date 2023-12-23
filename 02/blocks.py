from util import assert_equals, file_to_array

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def count_game(game_string):
    # Parse and return game
    parts = game_string.split(":")
    game = {
        "number": int(parts[0].split()[1]),
        "red": 0,
        "green": 0,
        "blue": 0,
    }

    for action in parts[1].split(";"):
        for block in action.split(","):
            block_details = block.split()
            game[block_details[1]] = max(game[block_details[1]], int(block_details[0]))
    return game


def match_colors(game, red, green, blue):
    return game["red"] <= red and game["green"] <= green and game["blue"] <= blue


def cube_power(game):
    return game["red"] * game["green"] * game["blue"]


def possible_games(filename, red, green, blue):
    lines = file_to_array(filename)
    games = [count_game(line) for line in lines]
    valid = [i for i in games if match_colors(i, red, green, blue)]
    return sum(game["number"] for game in valid)


def fewest_cubes(filename):
    lines = file_to_array(filename)
    games = [count_game(line) for line in lines]
    return sum(cube_power(game) for game in games)


assert_equals(possible_games(TEST_INPUT, 12, 13, 14), 8)
print("Part One: ", possible_games(INPUT, 12, 13, 14))
assert_equals(fewest_cubes(TEST_INPUT), 2286)
print("Part Two: ", fewest_cubes(INPUT))
