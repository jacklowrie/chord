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
    flag = True
    # for i in range(len(hosts)-1):
    #     host = hosts[i]
    #     if flag:
    #         host.cmd(f"python3 nodes/trace_test_anchor.py 10.0.0.1 {port} > /tmp/h{i}.log 2>&1 &")
    #         flag = False
    #     else:
    #         ip = host.IP()
    #         print(ip)
    #         host.cmd(f"python3 nodes/trace_test_joiner.py {ip} {port} 10.0.0.1 > /tmp/h{i}.log 2>&1 &")


    CLI(net)
    
    # Stop the network
    net.stop()

if __name__ == '__main__':
    run_mininet()  # Execute the network function

