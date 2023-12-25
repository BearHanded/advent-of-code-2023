import copy
import time
from util import assert_equals, file_to_array
from itertools import combinations
from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt

FILENAME = "input.txt"


INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


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

    cables = set() # set of sets
    unconnected = {}
    for name, component in network.items():
        for connection in component.connections:
            cable = (name, connection) if name < connection else (connection, name)
            cables.add(cable)
            if connection not in network:
                if connection not in unconnected:
                    unconnected[connection] = Component(connection, {name})
                unconnected[connection].connect(name)
                continue
            network[connection].connect(name)
    network.update(unconnected)

    visualize(network)
    # for item in network.values():
    #     print(item.stringify())


    # df = pd.read_csv('data.csv', sep=" ", header=None)/
    # plot.add_tools(PointDrawTool(renderers = [graph_renderer.node_renderer], empty_value = 'black'))
    # plot.renderers.append(graph_renderer)

    # # Start disconnecting
    # for connections in list(combinations(cables, 3)):
    #     test_network = copy.deepcopy(network)
    #     network_entry_points = []
    #     for cable in connections:
    #         test_network[cable[0]].connections.remove(cable[1])
    #         test_network[cable[1]].connections.remove(cable[0])
    #         network_entry_points += list(cable)
        
    #     # test networks
    #     checked = set()
    #     for entry in network_entry_points:
    #         check = 

    #     print (c1, c2, c3)


def visualize(network):
    G = nx.DiGraph()
    for name, component in network.items():
        G.add_node(name)
        G.add_edges_from((name, connection) for connection in component.connections)
    pos = nx.spring_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=120,
        node_color="skyblue",
        font_size=8,
    )
    plt.show()


# assert_equals(split_nodes(TEST_INPUT), 54)
start = time.time()
print("Part One: ", split_nodes(INPUT))
print(time.time() - start)
