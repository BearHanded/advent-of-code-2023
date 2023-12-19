from util import christmas_input

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'

def process(f):
    lines = christmas_input.file_to_subarray(f)
    sums = {
        "x": 0,
        "m": 0,
        "s": 0,
        "a": 0
    }
    rules = {}
    # Build Rules
    for workflow in lines[0]:
        chunks = workflow.split("{")
        steps = chunks[1][:-1].split(",")
        rules[chunks[0]] = [rule.split(":") for rule in steps] # [[comparison, destination],...,[destination]]

    # Start sorting
    for part in lines[1]:
        idx = "in"
        part_values = dict([(k, int(v)) for (k, v) in [i.split("=") for i in part[1:-1].split(",")]])

        # Evaluate
        while idx not in ["A", "R"]:
            rule_set = rules[idx]
            for rule in rule_set:
                if len(rule) == 1:
                    idx = rule[0]
                    break
                result = part_values[rule[0][0]] > int(rule[0][2:]) if rule[0][1] == ">" else part_values[key] < int(rule[0][2:])
                if result:
                    idx = rule[1]
                    break
            if idx == "A":
                for k, v in part_values.items():
                    sums[k] += v

    return sum(sums.values())

assert process(TEST_INPUT) == 19114
print("Part One: ", process(INPUT))
