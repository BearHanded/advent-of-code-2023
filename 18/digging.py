from util import christmas_input
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
TEST_INPUT_2 = 'test_input2.txt'

DIRECTIONS = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}
DIRECTION_NUM = ["R", "D", "L", "U"]


def shortest_path(f, translate_hex=False):
    commands = [(i, int(j), hex_to_command(k[2:-1])) for (i, j, k) in [row.split() for row in christmas_input.file_to_array(f)]]
    walls = {"L": set(), "R": set(), "U": set(), "D": set()}
    idx = (0, 0)
    for line in commands:
        command = line[2] if translate_hex else (line[0], line[1])
        direction = DIRECTIONS[command[0]]
        new_idx = (idx[0] + direction[0]*command[1], idx[1] + direction[1]*command[1])
        walls[command[0]].add((idx, new_idx))  # corner to corner
        idx = new_idx
    print(walls)

    area = 0
    print("CALCULATING")
    # INTERIOR
    for ((x, y1), (_, y2)) in walls["U"]:
        for y in range(y2, y1+1):
            # if another Up exists before a down to the left, skip, counted
            left_up = [left_x for ((left_x, left_y1), (_, left_y2)) in walls["U"] 
                                            if x > left_x and left_y2<= y <= left_y1]
            left_down = [left_x for ((left_x, left_y1), (_, left_y2)) in walls["D"] 
                                            if x > left_x and left_y1<= y <= left_y2]
            if len(left_up) and (len(left_down) == 0 or max(left_up) > max(left_down)):
                continue
            
            # Similar on the far side, if no other ups, max down. Else, get the max down before the next up
            next_downs = [down_x for ((down_x, down_y1), (_, down_y2)) in walls["D"] 
                if x < down_x and down_y1<= y <= down_y2]
            next_up = [up_x for ((up_x, up_y1), (_, up_y2)) in walls["U"] 
                                            if x < up_x and up_x > min(next_downs) and up_y2<= y <= up_y1]
            if len(next_up) == 0:
                wall_x = max(next_downs)
            else:
                wall_x = max([i for i in next_downs if i < min(next_up)])
            area += abs(wall_x - x) + 1
    print(area)
    return area

def hex_to_command(hex):
    return (DIRECTION_NUM[int(hex[-1])], int(hex[:-1], 16))


assert shortest_path(TEST_INPUT) == 62  # 38 outside, 24 inside
print("Part One: ", shortest_path(INPUT))
assert hex_to_command("70c710") == ("R", 461937)
assert shortest_path(TEST_INPUT, translate_hex=True) == 952408144115
# print("Part Two: ", shortest_path(INPUT, translate_hex=True))
