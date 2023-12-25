import time
from util import assert_equals, file_to_array
from z3 import Solver, Reals


INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


class Ray:
    def __init__(self, coordinates, direction_vector):
        self.x, self.y , self.z = coordinates
        self.dx, self.dy , self.dz = direction_vector

    def at_time(self, elapsed):
        return self.x + elapsed * self.dx, self.y + elapsed * self.dy, self.z + elapsed * self.dz


def find_path(f):
    lines = [[[int(j) for j in i.split(", ")] for i in row.split(" @ ")] for row in file_to_array(f)]
    hail = [Ray(p, d) for (p, d) in lines]

    solver = Solver()
    x, y, z = Reals("x y z")
    dx, dy, dz = Reals("dx dy dz")
    times = Reals("t1 t2 t3")

    eqs = []
    for ray, t in zip(hail[:3], times):
        eqs.append(x + t * dx == ray.x + t * ray.dx)
        eqs.append(y + t * dy == ray.y + t * ray.dy)
        eqs.append(z + t * dz == ray.z + t * ray.dz)
    solver.add(*eqs)

    solver.check()
    throw = solver.model()
    total = throw[x].as_long() + throw[y].as_long() + throw[z].as_long()
    return total


assert_equals(find_path(TEST_INPUT), 47)
start = time.time()
print("Part Two: ", find_path(INPUT))
print(time.time() - start)