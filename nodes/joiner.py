"""
makes a node, joins a specified ring, then drops into repl.
"""
import sys
import os

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
    
    code.interact(local=locals())
    node.stop()

if __name__ == '__main__':
    main()

