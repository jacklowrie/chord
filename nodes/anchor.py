""" creates a node and then starts the python repl.
Saves some time with manual testing.
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from chord import Node as ChordNode

def main():
    # Get IP and port from command line arguments
    ip = sys.argv[1]
    port = int(sys.argv[2])
    
    node = ChordNode(ip, port)
    node.create()


    code.interact(local=locals()) 

    node.stop()

if __name__ == '__main__':
    main()

