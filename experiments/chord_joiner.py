# run this from a host to join an existing chord ring.
# good for testing chord protocol with mininet.
import sys
import os
import signal
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from chord import Node as ChordNode

def main():
    # Get IP and port from command line arguments
    ip = sys.argv[1]
    port = int(sys.argv[2])
    known = sys.argv[3]
            
    # Create and join node
    node = ChordNode(ip, port)
    node.join(known, port)
    
    # Start the node
    print(f"Chord node started: {node.address}")
    print("To stop the node:")
    print("  - Press Ctrl+C")
    print("  - Send a SIGTERM signal")
    
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

if __name__ == '__main__':
    main()

