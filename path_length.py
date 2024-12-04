from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel
import time
import random
from src.chord.node import Node
from src.chord.address import Address

def setup_chord_ring(num_nodes=10, port=5000):
    net = Mininet(controller=Controller)

    c0 = net.addController('c0')
    s1 = net.addSwitch('s1')

    hosts = []
    nodes = []

    for i in range(1, num_nodes + 1):
        host = net.addHost(f'h{i}', ip=f'10.0.0.{i}')
        net.addLink(host, s1)
        hosts.append(host)

    net.start()

    print("\nInitializing Chord Ring...")

    h1 = hosts[0]
    h1.cmd(f"python3 tests/chk_join/anchor.py 10.0.0.1 {port} > /tmp/h1.log 2>&1 &")
    time.sleep(1)

    for i in range(1, len(hosts)):
        prev_host_ip = f"10.0.0.{i}"
        host_ip = f"10.0.0.{i+1}"
        hosts[i].cmd(f"python3 tests/chk_join/joiner.py {host_ip} {port} {prev_host_ip} > /tmp/h{i+1}.log 2>&1 &")
        node = Node(host_ip, port)
        nodes.append(node)
        time.sleep(1)

    print("\nChord Ring successfully created.")
    return net, nodes


def simulate_chord_query_with_fingers(start_node, target_key, hosts):
    """
    Simulate a Chord query using the finger table for efficient routing.

    Args:
        start_node: The starting node for the query.
        target_key: The hashed key of the target node being queried.
        hosts: List of all nodes in the Chord ring.

    Returns:
        Number of hops taken to resolve the query.
    """
    hops = 0
    current_node = start_node

    print(f"Starting query at {current_node.name}, looking for key {target_key}.")

    while True:
        hops += 1
        # Check if the current node is responsible for the target key
        if current_node.address.key == target_key:
        # if current_node.key == target_key:
            print(f"Resolved query at {current_node.name} in {hops} hops.")
            break

        # Find the closest preceding node using the finger table
        finger_table = current_node.finger_table
        for node, arr in finger_table:
            start, end = arr
            if start <= target_key < end:
                current_node = node
                break
        

    return hops



def get_closest_preceding_node(node, key, hosts):
    # Mock finger table lookup: replace with real logic
    return random.choice(hosts)


def simulate_queries(hosts, num_queries=5, port=5000):
    print("\nSimulating queries in the Chord ring...")
    for i in range(num_queries):
        start_node = random.choice(hosts)
        target_node = random.choice(hosts)
        target_key = target_node.address.key

        print(f"Query {i+1}: Start at {start_node.name}, Target Key {target_key} ({target_node.name})")
        hops = simulate_chord_query_with_fingers(start_node, target_key, hosts)
        print(f"Query {i+1} resolved in {hops} hops.")

    print("\nQueries completed.")




def main():
    setLogLevel('info')

    # Setup Chord ring with 10 nodes
    net, nodes = setup_chord_ring()
    print (nodes)
    for i in nodes:
        print ("address", i.address)
        print ("finger_table", i.finger_table)
    # print (hosts[0].successor)
    # Simulate queries in the Chord ring
    # simulate_queries(hosts, num_queries=1)

    # Start CLI for exploration
    CLI(net)

    # Stop the network
    net.stop()


if __name__ == '__main__':
    main()
