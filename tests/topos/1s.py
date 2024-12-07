from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel
import time
import sys

def run_mininet():
    # Set logging level to info
    setLogLevel('info')

    if len(sys.argv) != 2:
        print(f"usage: sudo python3 {sys.argv[0]} [num_hosts]")
        sys.exit(1)
    num_hosts = int(sys.argv[1])
    # set chord port
    port = 5000

    # activate
    start_venv = "source .venv/bin/activate"

    # Create a Mininet instance with a software switch
    net = Mininet(controller=Controller)

    c0 = net.addController('c0')

    # Create a switch
    s1 = net.addSwitch('s1')  # This adds a switch named s1

    # Add/link hosts
    print(f"making {num_hosts} hosts")
    hosts = []  # List to store Chord nodes
    for i in range(1, num_hosts + 1):
        # Add host to the network
        host = net.addHost(f'h{i}')
        net.addLink(host, s1)
        hosts.append(host)



    # Start the network
    net.start()

    CLI(net)
    
    # Stop the network
    net.stop()

if __name__ == '__main__':
    run_mininet()  # Execute the network function

