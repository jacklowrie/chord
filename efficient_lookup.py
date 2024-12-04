from mininet.net import Mininet
from mininet.node import Controller
from mininet.log import setLogLevel
import time
# from src.node import Node
# from .src.chord.node import Node
from src.chord.node import Node
import random


def setup_network_and_get_hashes():
    """
    Create a Mininet network, initialize Chord nodes, and get their hash values.
    """
    setLogLevel('info')

    num_hosts = 10  # Number of hosts
    port = 5000     # Port for Chord nodes
    net = Mininet(controller=Controller)

    # Add controller and switch
    c0 = net.addController('c0')
    s1 = net.addSwitch('s1')

    # Add hosts and initialize Chord nodes
    nodes = []  # List to store Chord nodes
    for i in range(1, num_hosts + 1):
        # Add host to the network
        host = net.addHost(f'h{i}')
        net.addLink(host, s1)
        nodes.append({"host": host, "node": None})  # Placeholder for Chord nodes

    # Start the Mininet network
    net.start()

    # Initialize Chord nodes after the network starts
    print("Chord Node Hashes:")
    for i, entry in enumerate(nodes, start=1):
        host = entry["host"]
        ip = host.IP()  # Get the host's IP
        chord_node = Node(ip=ip, port=port)  # Initialize the Chord node
        entry["node"] = chord_node

        # Print the IP and hash
        print(f"Node h{i} -> IP: {chord_node.address.ip}, Hash: {chord_node.address.key}")

    # Stop the network
    net.stop()




def simulate_single_query(start_host, target_host, target_hash):
    """
    Simulate a single Chord query between two hosts.
    :param start_host: Starting host for the query.
    :param target_host: Target host for the query.
    :param hosts: List of all hosts in the network.
    :return: Number of hops taken to resolve the query.
    """
    curr_node = start_host
    hops = 0
    while True:
        successor_node = curr_node.successor
        if curr_node.address.key <= target_hash < successor_node.address.key:
            break
        hops += 1
        curr_node = curr_node.lookup(target_hash)
        # for host in curr_node.finger_table:
        #     start, end = curr_node.finger_table[host]
        #     if start <= target_hash <= end:
        #         curr_node = host
    
    return hops


# def simulate_chord_query(hosts, num_queries=100):
#     """Simulate Chord queries and measure path lengths."""
#     path_lengths = []

#     for _ in range(num_queries):
#         start_host = np.random.choice(hosts)
#         target_key = np.random.randint(len(hosts))  # Simulating key in range of hosts

#         # Simulate querying and measure path length
#         current_host = start_host
#         hops = 0
    
#         while True:
#             hops += 1
#             current_id = int(current_host.IP().split('.')[-1])
#             target_id = target_key + 1  # Node IDs start from 1

#             if current_id == target_id:  # Query resolved
#                 break

#             # Simplified routing logic for the experiment
#             next_host_index = (current_id + 1) % len(hosts)  # Next hop
#             current_host = hosts[next_host_index]

#         path_lengths.append(hops)

#     return path_lengths chrome

target_hash = None

def setup_network(num_hosts=10, port=5000):
    """
    Set up a Mininet network and initialize Chord nodes.
    :param num_hosts: Number of hosts to create.
    :param port: Port number for Chord nodes.
    :return: List of initialized Chord nodes.
    """
    setLogLevel('info')

    net = Mininet(controller=Controller)

    # Add controller and switch
    c0 = net.addController('c0')
    s1 = net.addSwitch('s1')

    # Add hosts and initialize Chord nodes
    nodes = []
    for i in range(1, num_hosts + 1):
        host = net.addHost(f'h{i}')
        net.addLink(host, s1)
        ip = host.IP()
        node = Node(ip=ip, port=port)  # Initialize Chord node
        nodes.append(node)

    # Start the Mininet network
    net.start()

    # Print hashes for debugging
    print("Chord Node Hashes:")
    for i, node in enumerate(nodes, start=1):
        print(f"Node h{i} -> IP: {node.address.ip}, Hash: {node.address.key}")

    return net, nodes


def simulate_queries(nodes, num_queries=100):
    """
    Simulate queries on the Chord network and measure path lengths.
    :param nodes: List of Chord nodes.
    :param num_queries: Number of queries to simulate.
    :return: None
    """
    from src.chord.address import Address  # Import Address for _SPACE
    path_lengths = []

    for _ in range(num_queries):
        # Choose random start node and target key
        start_node = random.choice(nodes)
        target_key = random.randint(0, Address._SPACE - 1)  # Use Address._SPACE

        # Simulate the query and count hops
        hops = start_node.simulate_query(target_key)
        path_lengths.append(hops)

    # Calculate metrics
    mean_length = sum(path_lengths) / len(path_lengths)
    path_lengths.sort()
    percentile_1st = path_lengths[int(len(path_lengths) * 0.01)]
    percentile_99th = path_lengths[int(len(path_lengths) * 0.99)]

    print(f"Path Length Metrics (over {num_queries} queries):")
    print(f"Mean: {mean_length}")
    print(f"1st Percentile: {percentile_1st}")
    print(f"99th Percentile: {percentile_99th}")


if __name__ == "__main__":
    # Set up network
    num_hosts = 10
    net, nodes = setup_network(num_hosts=num_hosts)

    # Simulate queries and measure path lengths
    num_queries = 100
    simulate_queries(nodes, num_queries=num_queries)

    # Stop the network
    net.stop()
