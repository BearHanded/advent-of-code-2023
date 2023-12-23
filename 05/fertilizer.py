from util import assert_equals, file_to_array

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def find_nearest_points(filename):
    lines = file_to_array(filename)
    seeds = [int(i) for i in lines[0].split(" ")[1:]]
    layer_idx = 0
    maps = [[]]

    for line in lines[2:]:
        if line == '':
            layer_idx += 1
            maps.append([])
            continue
        elif "map" in line:
            continue
        maps[layer_idx].append([int(i) for i in line.split()])

    locations = [convert(seed, maps) for seed in seeds]
    return min(locations)


def find_nearest_range(filename):
    lines = file_to_array(filename)
    a = iter([int(i) for i in lines[0].split(" ")[1:]])
    seeds = [(i, i+k-1) for i, k in zip(a, a)]
    layer_idx = 0
    maps = [[]]

    for line in lines[2:]:
        if line == '':
            layer_idx += 1
            maps.append([])
            continue
        elif "map" in line:
            continue
        parsed = [int(i) for i in line.split()]
        maps[layer_idx].append([int(i) for i in line.split()])

    # Iterate through each layer and chunk into smaller ranges
    for layer in maps:
        next_level = []
        curr_level = seeds
        while len(curr_level) > 0:
            seed_lower, seed_upper = curr_level.pop()
            modified = False
            for entry in layer:
                if entry[1] <= seed_lower and seed_upper < (entry[1] + entry[2]):
                    # map contains seeds
                    next_level.append((shift_layer(seed_lower, entry), shift_layer(seed_upper, entry)))
                    modified = True
                    break
                elif seed_lower <= entry[1] and (entry[1] + entry[2]) < seed_upper:
                    # seeds contains map
                    next_level.append((entry[0], entry[0] + entry[2]))
                    curr_level.append((seed_lower, entry[1]-1))
                    curr_level.append((entry[1]+entry[2], seed_upper))
                    modified = True
                    break
                elif entry[1] <= seed_lower < (entry[1] + entry[2]):
                    # map overlaps lower seed
                    next_level.append((shift_layer(seed_lower, entry), entry[0] + entry[2]))
                    curr_level.append((entry[1]+entry[2], seed_upper))
                    modified = True
                    break
                elif entry[1] <= seed_upper < (entry[1] + entry[2]):
                    # map overlaps upper seed
                    next_level.append((entry[0], shift_layer(seed_upper, entry)))
                    curr_level.append((seed_lower, entry[1]-1))
                    modified = True
                    break
            if not modified:
                next_level.append((seed_lower, seed_upper))
        seeds = next_level

    return min([seed_lower for seed_lower, _ in seeds])


def convert(seed, maps):
    value = seed
    for layer in maps:
        for entry in layer:
            if entry[1] <= value < (entry[1] + entry[2]):
                value = shift_layer(value, entry)
                break
    return value


def shift_layer(value, entry):
    return value - entry[1] + entry[0]


assert_equals(find_nearest_points(TEST_INPUT), 35)
print("Part One: ", find_nearest_points(INPUT))

assert_equals(find_nearest_range(TEST_INPUT), 46)
print("Part Two: ", find_nearest_range(INPUT))

