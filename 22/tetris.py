from util import christmas_input
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'

def part_one(f):
    # Parse Bricks
    bricks = [tuple(tuple([int(c) for c in i.split(",")]) for i in row.split("~")) for row in christmas_input.file_to_array(f)]
    # bricks = dict([(i, brick) for (i, brick) in enumerate(bricks)])
    bricks = simulate(bricks)
    marked = find_disintegrations(bricks)
    return len(marked)


def simulate(bricks):
    falling = True
    while falling:
        falling = False  # if only python had a do while loop
        for idx in range(len(bricks)):  # we know our dict is indexed by #
            new_location = predict(bricks[idx], bricks)
            if new_location != bricks[idx]:
                falling = True
                bricks[idx] = new_location
    return bricks
        
def predict(b, bricks):
    z = 0  # ground level
    for x in range(b[0][0], b[1][0] + 1):
        for y in range(b[0][1], b[1][1] + 1):
            for b2 in bricks:
                if b == b2 or b[1][2] <= b2[1][2]:
                    continue
                if b2[0][0] <= x <= b2[1][0] and b2[0][1] <= y <= b2[1][1] : # Collision
                    z = max(z, b2[1][2])
    
    z_delta = min(b[0][2], b[1][2]) - z - 1 # Distance to block or ground
    if z_delta:
        return ((b[0][0], b[0][1], b[0][2] - z_delta), (b[1][0], b[1][1], b[1][2] - z_delta))
    return b


def find_disintegrations(bricks):
    # Build a map of what each brick is supported by
    # If a brick does not appears in any support set alone, continue
    return 0


assert part_one(TEST_INPUT) == 5
print("Part One: ", part_one(INPUT))
