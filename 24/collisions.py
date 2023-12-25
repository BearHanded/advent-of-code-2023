import time
from util import assert_equals, file_to_array

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


class Point:  # Default behavior is transparent broadcaster
    def __init__(self, coordinates):
        self.x, self.y , self.z  = coordinates

class Ray:  # Default behavior is transparent broadcaster
    def __init__(self, coordinates, direction_vector):
        self.x, self.y , self.z  = coordinates
        self.dx, self.dy , self.dz  = direction_vector


def test_collisions(min_range, max_range, f):
    lines = [[[int(j) for j in i.split(", ")] for i in row.split(" @ ")] for row in file_to_array(f)]
    hail = [Ray(p, d) for (p, d) in lines]

    intersections = 0
    for idx, a in enumerate(hail):
        for b in hail[idx+1:]:
            p = intersection_2d(a, b)
            if p and  min_range <= p[0] < max_range and min_range <= p[1] < max_range:
                intersections += 1

    return intersections


# https://stackoverflow.com/questions/2931573/determining-if-two-rays-intersect
def intersection_2d(a, b):
    if a == b: 
        return None
    dx = b.x - a.x
    dy = b.y - a.y
    det = b.dx * a.dy - b.dy * a.dx
    if det == 0:
        return None
    u = (dy * b.dx - dx * b.dy) / det
    v = (dy * a.dx - dx * a.dy) / det

    if u < 0 or v < 0:
        return None
    a.x + a.dx * u, a.y + a.dy * u
    return a.x + a.dx * u, a.y + a.dy * u


assert_equals(test_collisions(7, 27, TEST_INPUT), 2)
start = time.time()
print("Part One: ", test_collisions(200000000000000, 400000000000000, INPUT))
print(time.time() - start)