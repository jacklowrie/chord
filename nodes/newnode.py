"""
makes a node, then drops into repl.
"""
import sys
import os
import code

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from chord import Node as ChordNode

def main():
    # Get IP and port from command line arguments
    ip = sys.argv[1]
    port = int(sys.argv[2])
            
    # Create and join node
    node = ChordNode(ip, port)
    
    code.interact(local=locals())
    node.stop()

if __name__ == '__main__':
    main()

