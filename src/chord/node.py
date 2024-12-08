# node.py

from .address import Address
from .net import _Net

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

        self.address = Address(ip, port)
        
        # Network topology management
        self.successor = None
        self.predecessor = None
        self.finger_table = [None] * Address._M
        self._next = 0 # for fix_fingers (iterating through finger_table)
        
        # Networking
        self._net = _Net(ip, port, self._process_request)
        self.is_running = False
        


    def create(self):
        """
        Creates a new Chord ring with this node as the initial member.

        The node sets itself as its own successor and initializes the finger table.
        """
        self.predecessor = None
        self.successor = self.address
        self.start()
        self.fix_fingers()
    


    def join(self, known_ip, known_port):
        """
        Joins an existing Chord ring through a known node's IP and port.

        Args:
            known_ip (str): IP address of an existing node in the Chord ring.
            known_port (int): Port number of the existing node.
        """
        self.predecessor = None
        
        # Create an Address object for the known node
        known_node_address = Address(known_ip, known_port)
        
        try:
            # Send a find_successor request to the known node for this node's key
            response = self._net.send_request(
                known_node_address, 
                'FIND_SUCCESSOR', 
                self.address.key
            )
            
            if response:
                self.successor = self._parse_response(response)
            else:
                raise ValueError("Failed to find successor")
            
            self.start()
            self.fix_fingers()
            
            
        except Exception as e:
            print(f"Join failed: {e}")
            raise



    def fix_fingers(self):
        pass



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
        if closest_node == self.address:
            return self.successor

        # Forward request to closest preceding node via network
        try:
            response = self._net.send_request(
                closest_node, 
                'FIND_SUCCESSOR', 
                id
            )
            return self._parse_response(response)
        
        except Exception as e:
            print(f"Find successor failed: {e}")
            # Fallback to local successor if network request fails
            return self.successor


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
    


    def check_predecessor(self):
        """
        Checks if the predecessor node has failed.

        Sets predecessor to None if unresponsive.
        """
        if not self.predecessor:
            return

        try:
            # Try to send a simple request to the predecessor
            response = self._net._send_request(
                self.predecessor, 
                'PING'
            )
            
            # If no response or invalid response, consider node failed
            if not response or response != 'ALIVE':
                self.predecessor = None
        
        except Exception:
            # Any network error means the predecessor is likely down
            self.predecessor = None



    def stabilize(self):
        """
        Periodically verifies and updates the node's successor.

        This method ensures the correctness of the Chord ring topology.
        """
        # Pseudocode from the paper
        # x = successor's predecessor
        # if x is between this node and its successor
        #     set successor to x
        # notify successor about this node
        pass
    


    def notify(self, potential_predecessor):
        """
        Notifies the node about a potential predecessor.

        Args:
            potential_predecessor (ChordNode): Node that might be the predecessor.
        """
        pass



    def start(self):
        """
        Starts the Chord node's network listener.

        Begins accepting incoming network connections in a separate thread.
        """
        self._net.start()



    def stop(self):
        """
        Gracefully stops the Chord node's network listener.

        Closes the server socket and waits for the network thread to terminate.
        """
        self._net.stop()



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
    


    def _process_request(self, method, args):
        """
        Routes incoming requests to appropriate methods.

        Args:
            method (str): The method to be called.
            args (list): Arguments for the method.

        Returns:
            The result of the method call or an error message.
        """
        if method == "PING":
            return "ALIVE"
        elif method == 'FIND_SUCCESSOR':
            return self.find_successor(int(args[0]))
        elif method == 'GET_PREDECESSOR':
            return self.predecessor
        
        return "INVALID_METHOD"


    def _parse_response(self, response):
        """
        Parses a network response into an Address object. Only addresses are expected.

        Args:
            response (str): Serialized node address in "key:ip:port" format.

        Returns:
            Address: Parsed Address object.

        Raises:
            ValueError: If the response format is invalid.
        """
        parts = response.split(':')
        if len(parts) == 3:
            address = Address(parts[1], int(parts[2]))
            address.key = int(parts[0])

            return address
        else:
            raise ValueError("Invalid node address response format")



    def __repr__(self):
        """
        Provides a string representation of the Chord node.

        Returns:
            str: A descriptive string of the node's key properties.
        """

        return f"ChordNode(key={self.address.key})"


