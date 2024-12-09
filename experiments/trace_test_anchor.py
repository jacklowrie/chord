# run this from a host to make a new chord ring. 
# Good for simple testing of the chord protocol with mininet.
import sys
import os
import signal
import time
import threading 

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

    stabilize_thread = threading.Thread(target=stabilize_node, args=(node,), daemon=True)
    stabilize_thread.start()

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
