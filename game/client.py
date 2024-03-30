import os
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Lock



class Client:
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5000))
    ADDR = (HOST, PORT)
    
    def __init__(self, name="Player"):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.connect(self.ADDR)
        self.send(name)

        rc_thread = Thread(target=self.receive)
        rc_thread.start()
        self.lock = Lock()

    def send(self, data):
        pass

    def receive(self):
        pass

    def disconnect(self):
        self.send_message("{quit}")
