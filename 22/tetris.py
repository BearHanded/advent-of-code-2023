from util import christmas_input
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'

# Looking for 375
def part_one(f):
    # Parse Bricks
    bricks = [tuple(tuple([int(c) for c in i.split(",")]) for i in row.split("~")) for row in christmas_input.file_to_array(f)]
    bricks.sort(key=lambda tup: tup[0][2])
    bricks, supports = simulate(bricks)

    # print("Supports:")
    # for support in supports.items():
    #     print(support)
    marked = find_disintegrations(supports)
    # print(len(marked))
    # print("Marks:")
    # for mark in marked:
    #     print(mark)
    return len(marked)


def simulate(bricks):
    supports = {}
    for idx in range(len(bricks)): 
        new_location, collisions = predict(bricks[idx], bricks, idx)
        supports[new_location] = collisions
        if new_location != bricks[idx]:
            bricks[idx] = new_location
    return bricks, supports
        
def predict(b, bricks, curr_idx):
    z = 0  # ground level
    collisions = []
    settled = b

    for x in range(b[0][0], b[1][0] + 1):
        for y in range(b[0][1], b[1][1] + 1):
            for b2 in bricks[:curr_idx]:
                if b2[0][0] <= x <= b2[1][0] and b2[0][1] <= y <= b2[1][1] : # Collision / Supported by
                    collisions.append(b2)
                    z = max(z, b2[1][2])
    
    z_delta = b[0][2] - z - 1 # Distance to block or ground
    if z_delta:
        settled = ((b[0][0], b[0][1], b[0][2] - z_delta), (b[1][0], b[1][1], b[1][2] - z_delta))
    collisions = [i for i in collisions if i[1][2] == settled[0][2] - 1]  # compare top to bottom
    return settled, collisions


def find_disintegrations(supports):
    marked = set()
    for b in supports:
        critical = False
        for support_structure in supports.values():
            if len(support_structure) == 1 and b in support_structure:
                critical = True
                break
        if not critical:
            marked.add(b)

    return marked


assert part_one(TEST_INPUT) == 5
print("Part One: ", part_one(INPUT))
