from util import christmas_input
import queue

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
# LOGIC
# 
def flip_flop(f, presses, rx_break=False):
    parsed = [(k, dest.split(", ")) for k, dest in [line.split(" -> ") for line in christmas_input.file_to_array(f)]]
    modules = {}
    for module in parsed:
        if module[0] == BROADCASTER:
            modules[BROADCASTER] = MODULE_MAP[BROADCASTER](module[1])
        else:
            modules[module[0][1:]] = MODULE_MAP[module[0][0]](module[1])
    untyped = {}
    for name, module in modules.items():
        for destination in module.destinations:
            if destination not in modules:
                untyped[destination] = DebugModule()
                continue
            modules[destination].connect(name)
    modules.update(untyped)
    
    
    high_total = 0
    low_total = 0
    rx_found = False
    stack = queue.Queue()
    for k, v in modules.items():
        print(k, v, v.destinations)
    for i in range(presses):
        stack.put((LOW, BROADCASTER, "button"))
        if i % 1000 == 0:
            print("PRESS:", i)
        while not stack.empty():
            pulse_type, module, source = stack.get()
            if pulse_type == HIGH:
                high_total += 1
            elif pulse_type == LOW:
                low_total += 1

            if rx_break and module == "rx" and pulse_type == LOW:
                rx_found = True
                break

            next_pulse, next_destinations = modules[module].process(pulse_type, source)
            for destination in next_destinations: 
                stack.put((next_pulse, destination, module))
        if rx_break and rx_found:
            print("RX LOW PULSE FOUND AT BUTTON PRESS:", i+1)
            break

    return high_total * low_total


assert flip_flop(TEST_INPUT, 1000) == 32000000
assert flip_flop(TEST_INPUT_2, 1000) == 11687500
print("Part One: ", flip_flop(INPUT, 1000))
print("Part Two: ", flip_flop(INPUT, 1000000000000000, rx_break=True))

