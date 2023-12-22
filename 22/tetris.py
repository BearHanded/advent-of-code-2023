import copy
from util import christmas_input
import time

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'

def part_one(f):
    # Parse Bricks
    bricks = [tuple(tuple([int(c) for c in i.split(",")]) for i in row.split("~")) for row in christmas_input.file_to_array(f)]
    bricks.sort(key=lambda tup: tup[0][2])
    bricks, supports = simulate(bricks)
    marked = [i for i in find_disintegrations(supports)]
    return len(marked)

def part_two(f):
    # Parse Bricks
    bricks = [tuple(tuple([int(c) for c in i.split(",")]) for i in row.split("~")) for row in christmas_input.file_to_array(f)]
    bricks.sort(key=lambda tup: tup[0][2])
    bricks, supports = simulate(bricks)
    marked = [i for i in find_disintegrations(supports)]
    cascade_sum = plan_cascade(bricks, supports, marked)
            
    return cascade_sum

def simulate(bricks):
    supports = {}
    for idx in range(len(bricks)): 
        new_location, collisions = predict(bricks[idx], bricks, idx)
        supports[new_location] = collisions
        bricks[idx] = new_location
    return bricks, supports
        
def predict(b, bricks, curr_idx):
    z = 0  # ground level
    collisions = set()
    settled = b
    for x in range(b[0][0], b[1][0] + 1):
        for y in range(b[0][1], b[1][1] + 1):
            for b2 in bricks[:curr_idx]:
                if b2[0][0] <= x <= b2[1][0] and b2[0][1] <= y <= b2[1][1] : # Collision / Supported by
                    collisions.add(b2)
                    z = max(z, b2[1][2])
    
    z_delta = b[0][2] - z - 1 # Distance to block or ground
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


def plan_cascade(bricks, supports, marked):
    destroyable = copy.deepcopy(bricks)
    for item in marked:
        destroyable.remove(item)
    total = 0
    print(bricks)
    for b in destroyable:
        destroyed = set([b])
        idx = bricks.index(b)

        for b2 in bricks[idx+1:]:
            if set(supports[b2]).issubset(destroyed):
                destroyed.add(b2)
        print(destroyed)
        total += len(destroyed) - 1  # TODO: Note the - 1, we are tracking the destroyed

    print(total)
    return total

start = time.time()

assert part_one(TEST_INPUT) == 5
print("Part One: ", part_one(INPUT))
assert part_two(TEST_INPUT) == 7
print("Part Two: ", part_two(INPUT))

end = time.time()
print(end - start)

# NOT
# 87123
# 86496