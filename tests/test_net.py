import pytest
import socket
import threading
from unittest.mock import Mock, patch

from chord import _Net

def test_net_initialization():
    mock_handler = Mock()
    net = _Net('localhost', 8000, mock_handler)
    
    assert net._ip == 'localhost'
    assert net._port == 8000
    assert net._request_handler == mock_handler

@patch('socket.socket')
@patch('threading.Thread')
def test_net_start(mock_thread, mock_socket):
    mock_handler = Mock()
    net = _Net('localhost', 8000, mock_handler)
    
    net.start()
    
    # Verify socket was created and bound
    mock_socket.return_value.bind.assert_called_once_with(('localhost', 8000))
    mock_socket.return_value.listen.assert_called_once_with(5)
    
    # Verify thread was started
    mock_thread.assert_called_once_with(
        target=net._listen_for_connections,
        daemon=True
    )

def test_net_handle_connection():
    # Mock socket and request handler
    mock_socket = Mock()
    mock_handler = Mock(return_value="test_response")
    
    net = _Net('localhost', 8000, mock_handler)
    
    # Simulate receiving a request
    mock_socket.recv.return_value = b"TEST:arg1:arg2"
    
    net._handle_connection(mock_socket)
    
    # Verify handler was called correctly
    mock_handler.assert_called_once_with('TEST', ['arg1', 'arg2'])
    
    # Verify response was sent
    mock_socket.send.assert_called_once_with(b"test_response")
    
    # Verify socket was closed
    mock_socket.close.assert_called_once()

def test_net_stop():
    mock_handler = Mock()
    net = _Net('localhost', 8000, mock_handler)
    
    # Mock the thread and socket
    net.network_thread = Mock()
    net.server_socket = Mock()
    
    net.stop()
    
    # Verify socket was closed
    net.server_socket.close.assert_called_once()
    
    # Verify thread was joined
    net.network_thread.join.assert_called_once()
