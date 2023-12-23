from util import assert_equals, file_to_array
import queue
import numpy as np

INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
TEST_INPUT_2 = 'test_input2.txt'
HIGH = "HIGH"
LOW = "LOW"
BROADCASTER = "broadcaster"

class Module:  # Default behavior is transparent broadcaster
    def __init__(self, destinations):
        self.type = BROADCASTER
        self.destinations = destinations
        self.pulse_state = None

    def process(self, pulse_type, source):
        self.pulse_state = pulse_type
        return (self.pulse_state, self.destinations)
    def connect(self, connection_name):
        return

class FlipFlop(Module):
    def __init__(self, destinations):
        self.type = "%"
        self.destinations = destinations
        self.pulse_state = False

    def process(self, pulse_type, source):
        if pulse_type == LOW:
            self.pulse_state = not self.pulse_state
            return (HIGH if self.pulse_state else LOW, self.destinations)
        return (None, [])

class DebugModule(Module):
    def __init__(self, destinations=[]):
        self.type = "%"
        self.destinations = []
        self.pulse_state = False

    def process(self, pulse_type, source):
        self.pulse_state = False
        return (None, [])


class Conjunction(Module):
    def __init__(self, destinations):
        self.type = "&"
        self.destinations = destinations
        self.memory = {}
    
    def connect(self, connection_name):
        self.memory[connection_name] = LOW
        return
    
    def process(self, pulse_type, source):
        self.memory[source] = pulse_type
        return (LOW if LOW not in self.memory.values() else HIGH, self.destinations)  # NAND

MODULE_MAP = {
    "&": Conjunction,
    "%": FlipFlop,
    "broadcaster": Module
}

def find_rx(f):
    parsed = [(k, dest.split(", ")) for k, dest in [line.split(" -> ") for line in file_to_array(f)]]
    modules = {}
    untyped = {}
    cycles = {}

    # Build Modules
    for module in parsed:
        if module[0] == BROADCASTER:
            modules[BROADCASTER] = MODULE_MAP[BROADCASTER](module[1])
        else:
            modules[module[0][1:]] = MODULE_MAP[module[0][0]](module[1])
    for name, module in modules.items():
        for destination in module.destinations:
            if destination not in modules:
                untyped[destination] = DebugModule()
                continue
            modules[destination].connect(name)
    modules.update(untyped)
    
    # Run
    stack = queue.Queue()
    press = 0
    while True:
        press += 1
        stack.put((LOW, BROADCASTER, "button"))
        while not stack.empty():
            pulse_type, module, source = stack.get()
            next_pulse, next_destinations = modules[module].process(pulse_type, source)
            
            if "vd" in next_destinations and next_pulse == HIGH: # All must be high to trigger a low for vd -> rx
                cycles[module] = press
                if len(cycles.values()) == 4:
                    return np.lcm.reduce(list(cycles.values()))

            for destination in next_destinations: 
                stack.put((next_pulse, destination, module))


print("Part Two: ", find_rx(INPUT))

