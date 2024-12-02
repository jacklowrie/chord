import socket
import sys
import threading

class _Net:

    def __init__(self, ip, port, request_handler):
        self._ip = ip
        self._port = port
        self._request_handler = request_handler
        self._running = False
        self._network_thread = None

    def start(self):
        """
        Starts the Chord node's network listener.

        Begins accepting incoming network connections in a separate thread.
        """
        self._running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self._ip, self._port))
        self.server_socket.listen(5)
        
        # Start network listener in a separate thread
        self.network_thread = threading.Thread(
            target=self._listen_for_connections, 
            daemon=True
        )
        self.network_thread.start()
    


    def stop(self):
        """
        Gracefully stops the Chord node's network listener.

        Closes the server socket and waits for the network thread to terminate.
        """
        self._running = False
        if self.server_socket:
            self.server_socket.close()
        if self.network_thread:
            self.network_thread.join()



    def _listen_for_connections(self):
        """
        Continuously listens for incoming network connections.

        Accepts client connections and spawns a thread to handle each connection.
        """
        while self.is_running:
            try:
                client_socket, address = self.server_socket.accept()
                # Handle each connection in a separate thread
                threading.Thread(
                    target=self._handle_connection, 
                    args=(client_socket,), 
                    daemon=True
                ).start()
            except Exception as e:
                if self.is_running:
                    sys.stderr.write(f"Error accepting connection: {e}\n")
                    sys.stderr.flush()
    
    def _handle_connection(self, client_socket):
        """
        Processes an individual network connection.

        Args:
            client_socket (socket): The socket connection to handle.
        """
        try:
            # Receive request
            request = client_socket.recv(1024).decode()
            
            # Parse request
            method, *args = request.split(':')
            
            # Dispatch to appropriate method
            response = self._request_handler(method, args)
            
            # Send response
            client_socket.send(str(response).encode())
        except Exception as e:
            sys.stderr.write(f"Error handling connection: {e}\n")
            sys.stderr.flush()
        finally:
            client_socket.close()
    
    
