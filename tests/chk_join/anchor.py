# anchor.py
# run this from a host to make a new chord ring. 
# Good for simple testing of the chord protocol with mininet.
import sys
import os
import signal
import time
import threading 

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from chord import Node as ChordNode

def main():
    ip = sys.argv[1]
    port = int(sys.argv[2])

    node = ChordNode(ip, port)
    # create (start) the ring
    node.create()
    print(f"Node created and ring started: {node.address}", file=sys.stderr)

    # Setup signal handling for graceful shutdown
    def signal_handler(signum, frame):
        print(f"\nReceived signal {signum}. Stopping Chord node...")
        node.stop()
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal

    # Start periodic stabilization
    def periodic_stabilize():
        while True:
            node.stabilize()  # Perform stabilization
            time.sleep(2)  # Wait for 2 seconds before stabilizing again

    # Start stabilization in a separate thread to run in the background
    threading.Thread(target=periodic_stabilize, daemon=True).start()

    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        node.stop()
        sys.exit(0)

if __name__ == '__main__':
    main()

