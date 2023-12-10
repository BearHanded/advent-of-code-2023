from util import christmas_input

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def find_next(f):
    sets = [[int(i) for i in line.split(" ")] for line in christmas_input.file_to_array(f)]
    extrapolated_sum = 0
    for idx, series in enumerate(sets):
        magnitudes = [series]
        depth = 0
        while any(i != 0 for i in magnitudes[depth]):
            magnitudes.append([(magnitudes[depth][idx + 1] - val) for idx, val in enumerate(magnitudes[depth][:-1])])
            depth += 1

        depth -= 1  # down one level for processing, don't need special handling for 0, will always be 0 at [-1]
        while depth >= 0:
            new_val = magnitudes[depth][-1] + magnitudes[depth+1][-1]
            magnitudes[depth].append(new_val)
            depth -= 1
        extrapolated_sum += magnitudes[0][-1]
    return extrapolated_sum


def find_previous(f):
    sets = [[int(i) for i in line.split(" ")] for line in christmas_input.file_to_array(f)]
    extrapolated_sum = 0
    for idx, series in enumerate(sets):
        magnitudes = [series]
        depth = 0

        while any(i != 0 for i in magnitudes[depth]):
            magnitudes.append([(magnitudes[depth][idx + 1] - val) for idx, val in enumerate(magnitudes[depth][:-1])])
            depth += 1

        depth -= 1  # down one level for processing, don't need special handling for 0, will always be 0 at [-1]
        while depth >= 0:
            new_val = magnitudes[depth][0] - magnitudes[depth+1][0]
            magnitudes[depth].insert(0, new_val)
            depth -= 1
        extrapolated_sum += magnitudes[0][0]
    return extrapolated_sum


assert find_next(TEST_INPUT) == 114
print("Part One: ", find_next(INPUT))

assert find_previous(TEST_INPUT) == 2
print("Part Two: ", find_previous(INPUT))
