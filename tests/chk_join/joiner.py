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
            
    # initialize this node
    node = ChordNode(ip, port)
    print(f"node initialized: {node.address}", file=sys.stderr)

    # join existing ring
    print(f"joining node at {known}:{port}", file=sys.stderr)
    node.join(known, port)
    
    if address == node.successor:
        print("PASSED: joiner's successor is the anchor.")
    else:
        print("FAILED: joiner's successor is not the anchor.")
        printf("\texpected:{address}")
        printf("\tactual:  {node.successor}")

    
    print(f"notifying successor")
    valid_response = node.notify(node.successor)
    if valid_response:
        print("PASSED: notifying the successor receives a valid response")
    else:
        print("FAILED: notify went wrong.")
    
    sys.stdout.flush()
    # Setup signal handling for graceful shutdown
    def signal_handler(signum, frame):
        print(f"\nReceived signal {signum}. Stopping Chord node...")
        node.stop()
        sys.exit(0)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        node.stop()
        sys.exit(0)

if __name__ == '__main__':
    main()

