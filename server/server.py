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

        client_id = f"Client{len(self.clients) + 1}"
        self.clients.append(client_socket)
        self.client_names[client_socket] = client_id

        print(f"[+] {client_id} connected from {address}")
        client_socket.send(f"Welcome {client_id}! Waiting for another person...\n".encode())

        # Notify when both clients connected
        if len(self.clients) == 2:
            for client in self.clients:
                client.send(b"=== Chat ready! Both clients connected ===\n")

        try:
            while True:
                message = client_socket.recv(1024)
                if not message:
                    break

                # Process through BF
                interpreter = BFInterpreter(self.bf_code, debug=self.debug)
                processed = interpreter.run(message)

                # Add sender label and broadcast
                sender_name = self.client_names[client_socket]
                labeled_message = f"[{sender_name}]: {processed.decode('ascii', errors='ignore')}\n"

                # Send to all clients (including sender with "You" label)
                for client in self.clients:
                    if client == client_socket:
                        client.send(f"[You]: {processed.decode('ascii', errors='ignore')}\n".encode())
                    else:
                        client.send(labeled_message.encode())

        except Exception as e:
            print(f"[-] Error with {client_id}: {e}")
        finally:
            self.clients.remove(client_socket)
            if client_socket in self.client_names:
                del self.client_names[client_socket]
            client_socket.close()
            print(f"[-] {client_id} disconnected")

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