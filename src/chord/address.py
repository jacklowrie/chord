
class Address:
    """
    Represents a network address with a unique key in a distributed system.

    This class encapsulates the network location (IP and port) and a unique
    identifier (key) used for routing and comparison in Chord.

    Attributes:
        key (int): A unique identifier for the node in the distributed system.
        ip (str): The IP address of the node.
        port (int): The network port number of the node.

    Provides methods for equality comparison and string representation.
    """
    __slots__: ['key', 'ip', 'port']

    def __init__(self, key, ip, port):
        self.key = key
        self.ip = ip
        self.port = port
    

    def __eq__(self, other):
        if not isinstance(other, Address):
            return False
        return (self.ip == other.ip and 
                self.port == other.port and 
                self.key == other.key)
    

    def __repr__(self):
        return f"Address(key={self.key}, ip={self.ip}, port={self.port})"

