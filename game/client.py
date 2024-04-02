import os
import json
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from public.board import Board


class Client:
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5000))
    BUFF_SIZE = int(os.getenv("BUFF_SIZE", 512))
    ADDR = (HOST, PORT)

    def __init__(self, name="Player", code=None):
        self.board = Board(self)

        self.name = name
        self.code = code

        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.connect(self.ADDR)
        Thread(target=self.receive).start()

    def send(self, data):
        data = bytes(json.dumps(data), "utf8")
        self.server.send(data)

    def receive(self):
        while True:
            try:
                data = self.server.recv(self.BUFF_SIZE).decode()
                data = json.loads(data)
            except:
                self.disconnect()
                break

    def disconnect(self):
        print("Disconnect")
        self.server.close()
        del self
