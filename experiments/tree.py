from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.topolib import TreeTopo
import time
import sys

def run_mininet():
    # Set logging level to info
    setLogLevel('info')

    # set chord port
    port = 5000
    depth = int(sys.argv[1])
    # activate
    start_venv = "source .venv/bin/activate"

    # Create a Mininet instance with a software switch
    tree_topo = TreeTopo(depth=depth, fanout=2)
    net = Mininet(topo=tree_topo)


    # Start the network
    net.start()
    hosts = net.hosts
    anchor_ip = hosts[0].IP()

    i=1
    hosts[0].cmd(f"python3 experiments/trace_test_anchor.py {anchor_ip} {port} > /tmp/h{i}m.log 2>&1 &")
    for host in hosts[1:-1]:
        host.cmd(f"python3 experiments/trace_test_joiner.py {host.IP()} {port} {anchor_ip} > /tmp/h{i}m.log 2>&1 &")
        i += 1
    i+=1
    host = hosts[-1]
    
    host.cmd(f"python3 experiments/trace_test_averager.py {host.IP()} {port} {anchor_ip} > /tmp/h{i}n.log 2>&1 &")

    CLI(net)
    
    # Stop the network
    net.stop()

if __name__ == '__main__':
    run_mininet()  # Execute the network function

