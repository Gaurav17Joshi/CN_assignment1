import copy
import math

INF = math.inf

network = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 7},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 7, 'C': 1}
}

def initialize_distance_tables(topology):
    tables = {}
    for node in topology:
        table = {}
        for dest in topology:
            if dest == node:
                table[dest] = (0, node)  # cost to itself is zero; next hop is itself.
            elif dest in topology[node]:
                table[dest] = (topology[node][dest], dest)
            else:
                table[dest] = (INF, None)
        tables[node] = table
    return tables

# Function to print the routing table for a given node.
def print_table(node, table):
    print(f"Routing table for {node}:")
    print(f"{'Destination':<12}{'Cost':<8}{'Next Hop':<10}")
    for dest, (cost, next_hop) in sorted(table.items()):
        cost_str = f"{cost}" if cost != INF else "INF"
        next_hop_str = f"{next_hop}" if next_hop is not None else "-"
        print(f"{dest:<12}{cost_str:<8}{next_hop_str:<10}")
    print("\n")

def distance_vector_routing(topology):
    tables = initialize_distance_tables(topology)
    iteration = 0
    updated = True

    print("Initial Routing Tables:")
    for node, table in tables.items():
        print_table(node, table)

    # Continue iterations until no changes occur (convergence)
    while updated:
        iteration += 1
        print(f"--- Iteration {iteration} ---")
        updated = False
        new_tables = copy.deepcopy(tables)
        for node in topology:
            for neighbor in topology[node]:
                for dest in topology:
                    # Avoid loops: a node doesn't use a path that leads back to itself immediately.
                    current_cost = tables[node][dest][0]
                    cost_via_neighbor = tables[node][neighbor][0] + tables[neighbor][dest][0]
                    if cost_via_neighbor < current_cost:
                        new_tables[node][dest] = (cost_via_neighbor, neighbor)
                        updated = True
        tables = new_tables
        for node, table in tables.items():
            print_table(node, table)
        if not updated:
            print("No updates in this iteration. Convergence achieved.\n")
    return tables

if __name__ == "__main__":
    final_tables = distance_vector_routing(network)
    print("Final Converged Routing Tables:")
    for node, table in final_tables.items():
        print_table(node, table)
