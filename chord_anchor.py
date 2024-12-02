# run this from a host to make a new chord ring. 
# Good for simple testing of the chord protocol with mininet.
import sys
import os
import signal

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from chord import Node as ChordNode

def main():
    # Get IP and port from command line arguments
    ip = sys.argv[1]
    port = int(sys.argv[2])
    
    node = ChordNode(ip, port)
    node.create()


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
        signal.pause()  # Wait for a signal
    except KeyboardInterrupt:
        node.stop()
        sys.exit(0)

if __name__ == '__main__':
    main()

