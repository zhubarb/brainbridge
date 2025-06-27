import socket
import threading


class BrainChatClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('ascii', errors='ignore')
                if message:
                    print(f"\n< {message}")
                    print("> ", end="", flush=True)
            except:
                break

    def start(self):
        self.socket.connect((self.host, self.port))
        print(f"[*] Connected to BrainChat at {self.host}:{self.port}")
        print("[*] Type messages and press Enter. Type 'quit' to exit.\n")

        # Start receiver thread
        thread = threading.Thread(target=self.receive_messages, daemon=True)
        thread.start()

        # Send messages
        while True:
            message = input("> ")
            if message.lower() == 'quit':
                break
            self.socket.send(message.encode('ascii'))

        self.socket.close()


if __name__ == "__main__":
    client = BrainChatClient()
    client.start()