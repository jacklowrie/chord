# chk_join.py
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel
import time

def run_mininet():
    # Set logging level to info for mininet
    setLogLevel('info')

    port = 5000
    start_venv = "source .venv/bin/activate"
    testrt="tests/chk_join"

    # Create a Mininet instance with a software switch
    net = Mininet(controller=Controller)

    c0 = net.addController('c0')

    # Create a switch
    s1 = net.addSwitch('s1')  # This adds a switch named s1

    # Create two hosts
    h1 = net.addHost('h1', ip='10.0.0.1')  # Host 1 with IP 10.0.0.1
    h2 = net.addHost('h2', ip='10.0.0.2')  # Host 2 with IP 10.0.0.2

    # Link hosts to the switch
    net.addLink(h1, s1, latency=30)
    net.addLink(h2, s1, latency=30)


    # Start the network
    net.start()

    # start new ring
    h1.cmd(start_venv)
    h1.cmd(f"python {testrt}/anchor.py 10.0.0.1 {port} > /tmp/h1.log 2>&1 &")

    h2.cmd(start_venv)
    h2.cmd(f"python {testrt}/joiner.py 10.0.0.2 {port} 10.0.0.1 > /tmp/h2.log 2>&1 &")

    time.sleep(1) 
    # Start Mininet CLI for further testing
    # CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    run_mininet()  # Execute the network function