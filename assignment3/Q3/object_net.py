import math
import copy

INF = math.inf

class Node:
    def __init__(self, name):
        self.name = name
        self.routing_table = {}

    def initialize_table(self, topology):
        for dest in topology:
            if dest == self.name:
                self.routing_table[dest] = (0, self.name)
            elif dest in topology[self.name]:
                self.routing_table[dest] = (topology[self.name][dest], dest)
            else:
                self.routing_table[dest] = (INF, None)

    def update_table(self, nodes, topology):
        updated = False
        for dest in self.routing_table:
            if dest == self.name:
                continue
            current_cost, current_next = self.routing_table[dest]
            for neighbor in topology[self.name]:
                neighbor_cost, _ = self.routing_table.get(neighbor, (INF, None))
                cost_to_neighbor = topology[self.name][neighbor]
                potential_cost = cost_to_neighbor + nodes[neighbor].routing_table[dest][0]
                if potential_cost < current_cost:
                    current_cost, current_next = potential_cost, neighbor
                    updated = True
            self.routing_table[dest] = (current_cost, current_next)
        return updated

    def print_table(self):
        print(f"Routing table for {self.name}:")
        print(f"{'Destination':<12}{'Cost':<8}{'Next Hop':<10}")
        for dest in sorted(self.routing_table.keys()):
            cost, next_hop = self.routing_table[dest]
            cost_str = f"{cost}" if cost != INF else "INF"
            next_hop_str = next_hop if next_hop is not None else "-"
            print(f"{dest:<12}{cost_str:<8}{next_hop_str:<10}")
        print()

def distance_vector_simulation(topology):
    # Create Node instances for each node in the topology.
    nodes = {name: Node(name) for name in topology}

    # Initialize the routing table for each node.
    for node in nodes.values():
        node.initialize_table(topology)

    print("Initial Routing Tables:")
    for node in nodes.values():
        node.print_table()

    iteration = 0
    while True:
        iteration += 1
        print(f"--- Iteration {iteration} ---")
        any_update = False

        snapshot = {name: copy.deepcopy(node.routing_table) for name, node in nodes.items()}

        for name, node in nodes.items():
            for dest in node.routing_table:
                if dest == name:
                    continue
                current_cost, current_next = snapshot[name][dest]
                for neighbor in topology[name]:
                    cost_to_neighbor = topology[name][neighbor]
                    neighbor_cost = snapshot[neighbor][dest][0]
                    potential_cost = cost_to_neighbor + neighbor_cost
                    if potential_cost < current_cost:
                        current_cost, current_next = potential_cost, neighbor
                        any_update = True
                node.routing_table[dest] = (current_cost, current_next)
            node.print_table()

        if not any_update:
            print("No updates in this iteration. Convergence reached.\n")
            break

    print("Final Converged Routing Tables:")
    for node in nodes.values():
        node.print_table()

if __name__ == "__main__":
    topology = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 7},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 7, 'C': 1}
    }
    
    distance_vector_simulation(topology)
