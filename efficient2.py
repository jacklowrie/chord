from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel
from src.chord.node import Node  # Importing Node class
from src.chord.address import Address  # Importing Address class


def setup_static_network():
    """
    Set up a static Mininet network with 10 hosts, initialize the Chord ring, and return the network and nodes.
    :return: Tuple (net, nodes) where net is the Mininet object and nodes is a list of Node objects.
    """
    setLogLevel('info')

    port = 5000
    net = Mininet(controller=Controller)
    c0 = net.addController('c0')
    s1 = net.addSwitch('s1')  # Central switch

    # Create 10 hosts and their corresponding Chord nodes
    nodes = []
    ips = [f'10.0.0.{i}' for i in range(1, 11)]

    for i, ip in enumerate(ips):
        host = net.addHost(f'h{i+1}', ip=ip)
        net.addLink(host, s1)

        # Create Node using the host's IP
        node = Node(ip, port)
        nodes.append(node)

    net.start()

    # Initialize the Chord ring
    print("\nInitializing Chord Ring...")
    try:
        nodes[0].create()  # First node creates the ring
        for i in range(1, len(nodes)):
            nodes[i].join(nodes[0].address.ip, nodes[0].address.port)
    except Exception as e:
        print(f"Error during ring initialization: {e}")
        net.stop()
        raise

    # Print the Chord ring configuration
    print("\nChord Ring Configuration:")
    for node in nodes:
        print(f"Node: {node.address.ip} (Hash: {node.address.key}) -> Successor: {node.successor.key}")

    return net, nodes


def simulate_query_static(nodes):
    """
    Simulate a query in the static network from the first node to a target node.
    :param nodes: List of Chord nodes in the ring.
    """
    start_node = nodes[0]  # Start at the first node
    target_node = nodes[5]  # Target the sixth node
    target_hash = target_node.address.key

    print(f"\nSimulating query from Node {start_node.address.key} to target hash {target_hash}")

    current_node = start_node
    hops = 0

    while True:
        hops += 1
        if current_node._is_key_in_range(target_hash):
            # Found the target key
            break
        else:
            # Move to the next node in the ring (successor)
            current_node = current_node.find_successor(target_hash)

    print(f"Query resolved in {hops} hops.")

def setup_dynamic_ring(num_nodes):
    """
    Create a Chord ring with `num_nodes` dynamically using Mininet.
    :param num_nodes: Number of nodes in the ring.
    :return: Tuple (net, nodes) where net is the Mininet network and nodes are Chord nodes.
    """
    setLogLevel('info')

    port = 5000
    net = Mininet(controller=Controller)
    c0 = net.addController('c0')
    s1 = net.addSwitch('s1')  # Central switch

    nodes = []

    # Create hosts dynamically
    for i in range(1, num_nodes + 1):
        host = net.addHost(f'h{i}')  # Mininet assigns IP dynamically
        net.addLink(host, s1)

        # Retrieve the dynamically assigned IP address
        ip = f'10.0.0.{i}'  # Default Mininet IP assignment pattern
        node = Node(ip, port)
        nodes.append(node)

    net.start()
    print (nodes)
    print("\nInitializing Chord Ring...")

    try:
        # First node initializes the ring
        nodes[0].create()

        # Other nodes join the ring
        for i in range(1, len(nodes)):
            nodes[i].join(nodes[0].address.ip, nodes[0].address.port)

    except Exception as e:
        print(f"Error during ring initialization: {e}")
        net.stop()
        raise

    print("\nChord Ring Configuration:")
    for node in nodes:
        print(f"Node: {node.address.ip} (Hash: {node.address.key}) -> Successor: {node.successor.key}")

    return net, nodes


def main():
    # Set up the Mininet network and Chord ring

    net, nodes = setup_dynamic_ring(5)
    net, nodes = setup_static_network()

    # Simulate a query
    simulate_query_static(nodes)

    # Stop the network
    net.stop()


if __name__ == '__main__':
    main()
