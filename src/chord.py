import hashlib
import socket
import threading
import sys

class ChordNode:
    """Implements a Chord distributed hash table node.
    
    This is meant to run on a host and handle any chord-related
    traffic. Applications should make one instance of this class,
    then use the methods to manage/interact with other nodes on
    the chord ring.

    Attributes:
        ip (str): IP address of the node.
        port (int): Port number the node listens on.
        node_id (int): Unique identifier for the node in the Chord ring.
        successor (ChordNode): The next node in the Chord ring.
        predecessor (ChordNode): The previous node in the Chord ring.
        finger_table (list): Routing table for efficient lookup.
    """

    def __init__(self, ip, port):
        """
        Initializes a new Chord node.

        Args:
            ip (str): IP address for the node.
            port (int): Port number to listen on.
        """
        # Network identification
        self.ip = ip
        self.port = port
        
        # Hardcoded 16-bit hash space
        self.m = 16
        self.hash_space = 2 ** self.m
        
        # Node identifier based on IP:port
        self.node_id = self._hash(f"{ip}:{port}")
        
        # Network topology management
        self.successor = None
        self.predecessor = None
        self.finger_table = [None] * self.m
        self.next = 0 # for fix_fingers (iterating through finger_table)
        
        # Networking
        self.server_socket = None
        self.is_running = False
        self.network_thread = None
        
    def _hash(self, key):
        """
        Generates a consistent hash for identifiers.

        Args:
            key (str): Input string to hash.

        Returns:
            int: Hashed identifier within the hash space.
        """
        return int(hashlib.sha1(key.encode()).hexdigest(), self.m) % self.hash_space
    
    def create(self):
        """
        Creates a new Chord ring with this node as the initial member.

        The node sets itself as its own successor and initializes the finger table.
        """
        self.predecessor = None
        self.successor = self
        self.fix_fingers()
    
    def join(self, known_node):
        """
        Joins an existing Chord ring through a known node.

        Args:
            known_node (ChordNode): An existing node in the Chord ring.
        """
        self.predecessor = None
        # Use known node to find our successor
        self.successor = known_node.find_successor(self.node_id)
        
        # Initialize finger table
        self.fix_fingers()

    def find_successor(self, id):
        pass
 
    def fix_fingers(self):
        pass

