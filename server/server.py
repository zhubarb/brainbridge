import socket
import threading
import os
import argparse
from brainfuck.interpreter import BFInterpreter


class BrainChatServer:

    def __init__(self, bf_program_path, port=5555, debug=False):
        with open(bf_program_path, 'r') as f:
            self.bf_code = f.read()
        self.port = port
        self.debug = debug
        self.clients = []
        self.client_names = {}  # Track client names

    def handle_client(self, client_socket, address):
        # Enforce 1:1 chat - only 2 clients allowed
        if len(self.clients) >= 2:
            client_socket.send(b"Chat full - only 2 clients allowed for 1:1 chat\n")
            client_socket.close()
            return

        # Wait for client name first
        try:
            client_socket.send(b"Enter your name: ")
            name_data = client_socket.recv(1024).decode().strip()
            client_name = name_data if name_data else f"Anonymous{len(self.clients) + 1}"
        except:
            client_name = f"Client{len(self.clients) + 1}"

        self.clients.append(client_socket)
        self.client_names[client_socket] = client_name

        print(f"[+] {client_name} connected from {address}")
        client_socket.send(f"Welcome {client_name}! ".encode())

        if len(self.clients) == 1:
            client_socket.send(b"Waiting for another person...\n")
        else:
            # Notify both clients
            other_client = self.clients[0] if self.clients[1] == client_socket else self.clients[1]
            other_name = self.client_names[other_client]

            client_socket.send(f"Connected with {other_name}!\n".encode())
            other_client.send(f"\n{client_name} joined the chat!\n".encode())

            for client in self.clients:
                client.send(b"=== Chat ready! Start typing ===\n")

        try:
            while True:
                message = client_socket.recv(1024)
                if not message:
                    break

                # Process through BF
                interpreter = BFInterpreter(self.bf_code, debug=self.debug)
                processed = interpreter.run(message)

                # Send with proper labels
                for client in self.clients:
                    if client == client_socket:
                        client.send(f"[You]: {processed.decode('ascii', errors='ignore')}\n".encode())
                    else:
                        client.send(f"[{client_name}]: {processed.decode('ascii', errors='ignore')}\n".encode())

        except Exception as e:
            print(f"[-] Error with {client_name}: {e}")  # Changed from client_id to client_name
        finally:
            self.clients.remove(client_socket)
            if client_socket in self.client_names:
                del self.client_names[client_socket]
            client_socket.close()
            print(f"[-] {client_name} disconnected")  # Changed from client_id to client_name

            # Notify remaining client
            if self.clients:
                self.clients[0].send(b"\n=== Other client disconnected ===\n")

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', self.port))
        server.listen(5)
        print(f"[*] BrainChat Server listening on port {self.port}")
        print(f"[*] Using BF program: {self.bf_code[:50]}...")

        try:
            while True:
                client, address = server.accept()
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client, address)
                )
                thread.start()
        except KeyboardInterrupt:
            print("\n[!] Shutting down...")
            server.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--bf', default='brainfuck/programs/echo.bf')
    parser.add_argument('--port', type=int, default=5555)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    server = BrainChatServer(args.bf, args.port, args.debug)
    server.start()