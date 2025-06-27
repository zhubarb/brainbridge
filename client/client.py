import socket
import threading


class BrainChatClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.socket.connect((self.host, self.port))

        # Server prompts for name
        name_prompt = self.socket.recv(1024).decode()
        print(name_prompt, end='', flush=True)

        # Send name
        username = input()
        self.socket.send(username.encode() + b'\n')

        # Receive welcome message
        welcome = self.socket.recv(1024).decode()
        print(welcome)

        # Start receiver thread
        thread = threading.Thread(target=self.receive_messages, daemon=True)
        thread.start()

        # Send messages
        while True:
            message = input()
            if message.lower() == 'quit':
                break
            self.socket.send(message.encode('ascii'))

        self.socket.close()

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('ascii', errors='ignore')
                if message:
                    print(f"{message}", end='', flush=True)
            except:
                break


if __name__ == "__main__":
    client = BrainChatClient()
    client.start()