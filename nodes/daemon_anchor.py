""" creates a node and then starts the python repl.
Saves some time with manual testing.
"""
import sys
import os
import code
import threading
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from chord import Node as ChordNode

def stabilize_node(node):
    while True:
        node.stabilize()
        node.fix_fingers()
        time.sleep(1)  # Call stabilize every 2 seconds

def main():
    # Get IP and port from command line arguments
    ip = sys.argv[1]
    port = int(sys.argv[2])
    
    node = ChordNode(ip, port)
    node.create()

    # Start the stabilize function in a separate thread
    stabilize_thread = threading.Thread(target=stabilize_node, args=(node,), daemon=True)
    stabilize_thread.start()

    code.interact(local=locals()) 

    node.stop()

if __name__ == '__main__':
    main()

