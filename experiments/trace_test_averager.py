# run this from a host to join an existing chord ring.
# good as a background process.
import sys
import os
import signal
import time
import threading
# from . import Address  # Ensure Address is imported
# from src.chord.address import Address

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from chord import Node as ChordNode

def stabilize_node(node):
    while True:
        time.sleep(1)
        node.stabilize()
        node.fix_fingers()

def trace_all_keys(node, output_file):
    """
    Traces successors for all keys in the hash space and logs hops.
    """
    # with open(output_file, 'w') as f:
    #--
    for key in range(2 ** 16):  # Iterate over entire hash space
        successor, hops = node.trace_successor(key, 0)
        print (f"{key}:{hops}", file=sys.stderr)
        


def main():
    # Get IP and port from command line arguments
    ip = sys.argv[1]
    port = int(sys.argv[2])
    known = sys.argv[3]
            
    # Create and join node
    node = ChordNode(ip, port)
    node.join(known, port)

    stabilize_thread = threading.Thread(target=stabilize_node, args=(node,), daemon=True)
    stabilize_thread.start()

    # Setup signal handling for graceful shutdown
    def signal_handler(signum, frame):
        # print(f"\nReceived signal {signum}. Stopping Chord node...")
        node.stop()
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal
    time.sleep(16) # let the fingertable populate
    

    output_file = f"/tmp/trace_results_{ip}_{port}.log"
    trace_all_keys(node, output_file)





    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        node.stop()

if __name__ == '__main__':
    main()

