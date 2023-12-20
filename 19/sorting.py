from util import christmas_input

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
MIN_NUM = 1
MAX_NUM = 4000


def process(f):
    lines = christmas_input.file_to_subarray(f)
    sums = {
        "x": 0,
        "m": 0,
        "a": 0,
        "s": 0
    }
    rules = build_rules(lines[0])

    for part in lines[1]:
        idx = "in"
        part_values = dict([(k, int(v)) for (k, v) in [i.split("=") for i in part[1:-1].split(",")]])
        while idx not in ["A", "R"]:
            rule_set = rules[idx]
            for rule in rule_set:
                if len(rule) == 1:
                    idx = rule[0]
                    break
                result = part_values[rule[0][0]] > int(rule[0][2:]) if rule[0][1] == ">" else part_values[rule[0][0]] < int(rule[0][2:])
                if result:
                    idx = rule[1]
                    break
            if idx == "A":
                for k, v in part_values.items():
                    sums[k] += v
    return sum(sums.values())


def total_allowed(f):
    rules = build_rules(christmas_input.file_to_subarray(f)[0])
    start_ranges = {
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000)
    }
    return get_solution_size("in", rules, start_ranges)


def get_solution_size(rule_key, rules, ranges):
    if rule_key == "A":
        solution_size = 1
        for (start, end) in ranges.values():
            solution_size *= end - start + 1
        return solution_size
    if rule_key == "R":
        return 0
        
    total = 0
    for rule in rules[rule_key]:
        next_ranges = ranges.copy()
        if len(rule) == 1:
            total += get_solution_size(rule[0], rules, next_ranges)
            break
        key = rule[0][0]
        value = int(rule[0][2:])
        (start, end) = next_ranges[key]

        if rule[0][1] == "<":
            if value < start:  # no satisfying values
                continue
            elif start < value < end:  # keep start -> value
                next_ranges[key] = (start, value-1)
                ranges[key] = (value, end)
            elif end < value:
                total += get_solution_size(rule[1], rules, next_ranges)  # consume the whole thing
                break
        else: 
            if end < value:  # no satisfying values
                continue
            elif start < value < end:  # keep start -> value
                next_ranges[key] = (value+1, end)
                ranges[key] = (start, value)
            elif value < start:  # consume the whole thing
                total += get_solution_size(rule[1], rules, next_ranges)  # consume the whole thing
                break
        total += get_solution_size(rule[1], rules, next_ranges)
    return total


def build_rules(rule_strings):
    rules = {}
    for workflow in rule_strings:
        chunks = workflow.split("{")
        rules[chunks[0]] = [rule.split(":") for rule in chunks[1][:-1].split(",")]
    return rules


assert process(TEST_INPUT) == 19114
print("Part One: ", process(INPUT))
assert total_allowed(TEST_INPUT) == 167409079868000
print("Part Two: ", total_allowed(INPUT))
