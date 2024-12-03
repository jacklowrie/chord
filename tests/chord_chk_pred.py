# chord_chk_pred.py
#
# this is meant to confirm that nodes can communicate
# over a network (i.e. mininet).
#
# run this from a host. pass in an existing node's IP.
#
# this makes a new node, sets it's pred to that existing node,
# then calls check_predecessor.
# good for testing chord protocol with mininet.
#
# NOTE: THIS IS NOT A FUNCTIONAL EXAMPLE OF CHORD! It's 
# an integration test.
import sys
import os
import code

sys.path.append(os.path.join(os.path.dirname(__file__), '..',  'src'))
from chord import Node as ChordNode
from chord import Address

def main():
    # Get IP and port from command line arguments
    ip = sys.argv[1]
    port = int(sys.argv[2])
    known = sys.argv[3]
    address = Address(known, port)
            
    # Create and join node
    node = ChordNode(ip, port)
    node.start()

    # try pinging the predecessor when it's None
    print("checking None")
    node.check_predecessor()
    if not node.predecessor:
        print("\tnode predecessor is still None!")
    else:
        print(f"\tpredecessor is no longer None. it is {node.predecessor}")

    # try pinging the predecessor when it's correct
    print("checking valid predecessor:")
    node.predecessor = address
    node.check_predecessor()
    if address == node.predecessor:
        print("\tsuccessfully pinged existing predecessor!")
    else:
        print(f"\tcould not ping existing predecessor: {address}")

    #try pinging the predecessor when it's unreachable
    print("checking down predecessor:")
    address = Address("10.0.0.3", port) # this assumes this IP/port combo is down
    node.predecessor = address
    node.check_predecessor()
    if not node.predecessor:
        print("\tsuccessfully removed down predecessor!")
    else:
        print(f"\tpredecessor never updated to None. it is {node.predecessor}")
    
    code.interact(local=locals())
    node.stop()

if __name__ == '__main__':
    main()

