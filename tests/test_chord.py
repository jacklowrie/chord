# test_node.py
import pytest
from unittest.mock import Mock, patch
from chord import Node as ChordNode
from chord import Address

@pytest.fixture
def mock_net():
    """Create a mock network layer for testing."""
    with patch('chord._Net') as MockNet:
        mock_net_instance = Mock()
        MockNet.return_value = mock_net_instance
        yield mock_net_instance

@pytest.fixture
def node(mock_net):
    """Create a Chord node with mocked network layer."""
    node = ChordNode('1.2.3.4', 5000)
    # Patch the start method to prevent actual network binding
    with patch.object(node, 'start', return_value=None):
        yield node

def test_join_successful(node, mock_net):
    """Test successful join to an existing Chord ring."""
    # Setup mock for send_request to simulate finding successor
    known_node = Address('5.6.7.8', 8000)
    mock_net.send_request.return_value = f"{known_node.key}:{known_node.ip}:{known_node.port}"
    
    # Perform join
    node.join('5.6.7.8', 8000)
    
    # Assertions
    assert node.successor == known_node
    mock_net.send_request.assert_called_once()

def test_join_failure(node, mock_net):
    """Test join failure scenario."""
    # Setup mock to simulate join failure
    mock_net.send_request.return_value = None
    
    # Expect an exception when join fails
    with pytest.raises(ValueError, match="Failed to find successor"):
        node.join('5.6.7.8', 8000)

def test_find_successor_local(node):
    """Test find_successor when the key is in local range."""
    node.address.key = 50
    node.successor = Address('1.2.3.4', 6000)
    node.successor.key = 100
    
    # Key is between node and successor
    result = node.find_successor(75)
    assert result == node.address

def test_find_successor_remote(node, mock_net):
    """Test find_successor when routing through another node."""
    # Setup node state
    node.address.key = 50
    node.successor = Address('1.2.3.4', 6000)
    node.successor.key = 200
    
    # Mock closest preceding node
    closest_node = Address('5.6.7.8', 7000)
    closest_node.key = 100
    node.closest_preceding_node = Mock(return_value=closest_node)
    
    # Mock network request for remote successor lookup
    remote_successor = Address('9.10.11.12', 9000)
    remote_successor.key = 250
    mock_net.send_request.return_value = f"{remote_successor.key}:{remote_successor.ip}:{remote_successor.port}"
    
    # Perform find_successor for a key outside local range
    result = node.find_successor(225)
    
    assert result == remote_successor
    mock_net.send_request.assert_called_once()

def test_check_predecessor_responsive(node, mock_net):
    """Test check_predecessor with a responsive predecessor."""
    # Setup a predecessor
    predecessor = Address('5.6.7.8', 8000)
    node.predecessor = predecessor
    
    # Mock network response
    mock_net.send_request.return_value = 'ALIVE'
    
    # Run check
    node.check_predecessor()
    
    # Predecessor should remain unchanged
    assert node.predecessor == predecessor
    mock_net.send_request.assert_called_once_with(predecessor, 'PING')

def test_check_predecessor_unresponsive(node, mock_net):
    """Test check_predecessor with an unresponsive predecessor."""
    # Setup a predecessor
    predecessor = Address('5.6.7.8', 8000)
    node.predecessor = predecessor
    
    # Mock network response to simulate unresponsive node
    mock_net.send_request.return_value = None
    
    # Run check
    node.check_predecessor()
    
    # Predecessor should be set to None
    assert node.predecessor is None

# Additional tests can be added for other complex methods like stabilize(), notify(), etc.

