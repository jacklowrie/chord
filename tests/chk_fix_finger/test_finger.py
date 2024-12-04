from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel
import time

def run_mininet():
    # Set logging level to info
    setLogLevel('info')

    # set chord port
    port = 5000

    # activate
    start_venv = "source .venv/bin/activate"

    # Create a Mininet instance with a software switch
    net = Mininet(controller=Controller)

    c0 = net.addController('c0')

    # Create a switch
    s1 = net.addSwitch('s1')  # This adds a switch named s1

    # Create two hosts
    h1 = net.addHost('h1', ip='10.0.0.1')  # Host 1 with IP 10.0.0.1
    h2 = net.addHost('h2', ip='10.0.0.2')  # Host 2 with IP 10.0.0.2

    # Link hosts to the switch
    net.addLink(h1, s1)
    net.addLink(h2, s1)


    # Start the network
    net.start()

    # start new ring
    h1.cmd(start_venv)

    h2.cmd(start_venv)
    print(f"test for the fix_finger begins")
    # Log finger table for all nodes using chord_fix_finger.py
    h1.cmd(f"python tests/chk_fix_finger/chord_fix_finger.py 10.0.0.1 {port} > /tmp/h1_fix_finger.log 2>&1 &")
    h2.cmd(f"python tests/chk_fix_finger/chord_fix_finger.py 10.0.0.2 {port} > /tmp/h2_fix_finger.log 2>&1 &")

    print("Observing network behavior for 5 seconds...")
    time.sleep(5)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    run_mininet()  # Execute the network function

