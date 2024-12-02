import hashlib

from .address import Address

class Node:
    """Implements a Chord distributed hash table node.
    
    This is meant to run on a host and handle any chord-related
    traffic. Applications should make one instance of this class,
    then use the methods to manage/interact with other nodes on
    the chord ring.

    Attributes:
        address (Address): node address info (key, ip, port).
        successor (Address): The next node in the Chord ring.
        predecessor (Address): The previous node in the Chord ring.
        finger_table (list): Routing table for efficient lookup.
    """

    def __init__(self, ip, port):
        """
        Initializes a new Chord node.

        Args:
            ip (str): IP address for the node.
            port (int): Port number to listen on.
        """

        # Hardcoded 16-bit hash space
        self.m = 16
        self.hash_space = 2 ** self.m

        # Network identification
        self.address = Address(self._hash(f"{ip}:{port}"), ip, port)
        
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
        self.successor = self.address
        self.fix_fingers()
    


    def join(self, known_node):
        """
        Joins an existing Chord ring through a known node.

        Args:
            known_node (ChordNode): An existing node in the Chord ring.
        """
        self.predecessor = None
        # Use known node to find our successor
        self.successor = known_node.find_successor(self.key)
        
        # Initialize finger table
        self.fix_fingers()



    def find_successor(self, id):
        """
        Finds the successor node for a given identifier.

        Args:
            id (int): Identifier to find the successor for.

        Returns:
            Address: The address of the node responsible for the given identifier.
        """
        # If id is between this node and its successor
        if self._is_key_in_range(id):
            return self.address
        
        # Find closest preceding node to route through
        closest_node = self.closest_preceding_node(id)
        
        # If closest node is self, return successor
        if closest_node is self:
            return self.successor
        
        # Forward request to closest preceding node
        return closest_node.find_successor(id)
    


    def _is_key_in_range(self, key):
        """
        Checks if a key is within the node's range.

        Args:
            key (int): Identifier to check.

        Returns:
            bool: True if the key is in the node's range, False otherwise.
        """
        if not self.successor: # no successor case
            return True
        
        successor_key = self.successor.key
        
        if self.address.key < successor_key:
            # Normal case: key is strictly between node and successor
            return self.address.key < key < successor_key
        else:  # Wrap around case
            return key > self.address.key or key < successor_key



    def closest_preceding_node(self, id):
        """
        Finds the closest preceding node for a given identifier.

        Args:
            id (int): Identifier to find the closest preceding node for.

        Returns:
            Address: The address of closest preceding node in the finger table.
        """
        # Search finger table in reverse order
        for finger in reversed(self.finger_table):
            if finger and self._is_between(self.address.key, id, finger.key):
                return finger
        
        # If no node found, return self
        return self.address
    
    

    def _is_between(self, start, end, key):
        """
        Checks if a node is between two identifiers in the Chord ring.

        Args:
            start (int): Starting identifier.
            end (int): Ending identifier.
            key (int): Node identifier to check.

        Returns:
            bool: True if the node is between start and end, False otherwise.
        """
        if start < end:
            return start < key < end
        else:  # Wrap around case
            return key > start or key < end
    
    

    def fix_fingers():
        pass



    def __repr__(self):
        """
        Provides a string representation of the Chord node.

        Returns:
            str: A descriptive string of the node's key properties.
        """

        return f"ChordNode(key={self.address.key})"


