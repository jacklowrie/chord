"""
makes a node, joins a specified ring, then drops into repl.
"""
import sys
import os
import code
import time
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from chord import Node as ChordNode

def stabilize_node(node):
    while True:
        time.sleep(1)
        node.stabilize()
        node.fix_fingers()

def main():
    # Get IP and port from command line arguments
    ip = sys.argv[1]
    port = int(sys.argv[2])
    known = sys.argv[3]
            
    # Create and join node
    node = ChordNode(ip, port)
    node.join(known, port)

    # Start the stabilize function in a separate thread
    stabilize_thread = threading.Thread(target=stabilize_node, args=(node,), daemon=True)
    stabilize_thread.start()
    
    code.interact(local=locals())
    node.stop()

if __name__ == '__main__':
    main()

