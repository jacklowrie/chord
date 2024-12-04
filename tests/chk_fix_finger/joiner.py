import sys
import os
import signal
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..','src'))
from chord import Node as ChordNode

def main():
    # Get IP and port from command line arguments
    ip = sys.argv[1]
    port = int(sys.argv[2])
    known = sys.argv[3]
    
    # Create a Node instance
    node = ChordNode(ip, port)
    node.join(known, port)
    
    # Log the finger table periodically
    def log_table_periodically():
        while True:
            node.log_finger_table()
            time.sleep(0.8)  # Log every 10 seconds

    # Handle signals for graceful shutdown
    def signal_handler(signum, frame):
        print(f"\nReceived signal {signum}. Stopping logging...")
        sys.exit(0)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal

    # Start logging in a separate thread
    try:
        log_table_periodically()
    except KeyboardInterrupt:
        print("Stopping logging...")
        sys.exit(0)

if __name__ == '__main__':
    main()

