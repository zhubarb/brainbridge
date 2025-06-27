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

    def handle_client(self, client_socket, address):
        print(f"[+] {address} connected")
        self.clients.append(client_socket)

        try:
            while True:
                message = client_socket.recv(1024)
                if not message:
                    break

                # Process through BF
                interpreter = BFInterpreter(self.bf_code, debug=self.debug)
                processed = interpreter.run(message)

                # Broadcast to all clients
                for client in self.clients:
                    try:
                        client.send(processed)
                    except:
                        pass

        except Exception as e:
            print(f"[-] Error with {address}: {e}")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()
            print(f"[-] {address} disconnected")

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