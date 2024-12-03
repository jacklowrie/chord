# joiner.py
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

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
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
    
    print(f"joining node at {known}:{port}")
    node.join(known, port)
    
    if address == node.successor:
        print("PASSED: joiner's successor is the anchor.")
    else:
        print("FAILED: joiner's successor is not the anchor.")
        printf("\texpected:{address}")
        printf("\tactual:  {node.successor}")

    
    node.stop()

if __name__ == '__main__':
    main()

