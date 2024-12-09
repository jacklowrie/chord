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
        if (i % 10==0):
            print ("Making host : ", i)

        # Add host to the network
        host = net.addHost(f'h{i}')
        net.addLink(host, s1)
        hosts.append(host)



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

