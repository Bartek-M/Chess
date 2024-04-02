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
        self.send({"type": "hello", "name": self.name, "code": self.code})

    def send(self, data):
        data = bytes(json.dumps(data), "utf8")
        self.server.send(data)

    def receive(self):
        while True:
            try:
                data = self.server.recv(self.BUFF_SIZE).decode("utf-8")
                data = json.loads(data)

                match data.get("type"):
                    case "hello":
                        self.code = data.get("code")
                    case "connect":
                        players = data.get("players", ("Player 2", self.name))
                        color = data.get("color", "w")
                        self.board.reset(players, color)
                    case "move":
                        pass
                    case "win":
                        pass
                    case "disconnect":
                        pass
            except:
                self.disconnect()
                break

    def disconnect(self):
        print("Disconnect")
        self.server.close()
        del self
