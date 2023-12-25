import heapq
import time
from util import assert_equals, file_to_array
import networkx as nx
import matplotlib.pyplot as plt

FILENAME = "input.txt"


INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
RENDER = False


class Component:  # Default behavior is transparent broadcaster
    def __init__(self, name, connections=set()):
        self.name = name
        self.connections = set(connections)

    def connect(self, component):
        self.connections.add(component)

    def stringify(self):
        return f"{self.name} -> {self.connections}"


def split_nodes(f):
    lines = [row.split(": ") for row in file_to_array(f)]
    network = {}

    for row in lines:
        component, connections = row
        network[component] = Component(component, connections.split(" "))

    # cables = set() # set of sets
    unconnected = {}
    for name, component in network.items():
        for connection in component.connections:
            # cable = (name, connection) if name < connection else (connection, name)
            # cables.add(cable)
            if connection not in network:
                if connection not in unconnected:
                    unconnected[connection] = Component(connection, {name})
                unconnected[connection].connect(name)
                continue
            network[connection].connect(name)
    network.update(unconnected)

    visualize(network)
    cuts = [("jzj", "vkb"), ("hhx", "vrx"), ("grh", "nvh")] # p1
    slice_network(network, cuts)
    visualize(network)

    size_a = count_network("jzj", network)
    size_b = count_network("vkb", network)

    assert (size_a + size_b) == len(network)
    return size_a * size_b


def slice_network(network, cuts):
    for a, b in cuts:
        network[a].connections.remove(b)
        network[b].connections.remove(a)


def count_network(entry, network):
    visited = {entry}
    queue = [entry]

    while len(queue) > 0:
        node = heapq.heappop(queue)
        for move in network[node].connections:
            if move not in visited:
                heapq.heappush(queue, move)
                visited.add(move)
    return len(visited)


def visualize(network):
    if not RENDER:
        return
    print(" Rendering...")
    G = nx.DiGraph()
    for name, component in network.items():
        G.add_node(name)
        G.add_edges_from((name, connection) for connection in component.connections)
    pos = nx.spring_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
    )
    plt.show()


# assert_equals(split_nodes(TEST_INPUT), 54)
start = time.time()
print("Part One: ", split_nodes(INPUT))
print(time.time() - start)
