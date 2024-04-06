import os
import json
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from public.board import Board
from public.utils import translate_pos


class Client:
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5000))
    BUFF_SIZE = int(os.getenv("BUFF_SIZE", 512))
    ADDR = (HOST, PORT)

    def __init__(self, name="Player", code=None):
        self.board = Board(self)

        self.name = name
        self.code = code
        self.end_text = None

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
            except:
                break

            data_type = data.get("type")

            if data_type == "hello":
                self.code = data.get("code")
            elif data_type == "connect":
                players = data.get("players", ("Player 2", self.name))
                color = data.get("color", "w")
                self.board.reset(players, color)
            elif data_type == "move":
                piece_pos = data.get("piece")
                pos = data.get("pos")

                if not (piece_pos and pos):
                    continue
                if self.board.color == "b":
                    piece_pos = translate_pos(piece_pos)
                    pos = translate_pos(pos)

                row, col = piece_pos
                piece = self.board.board[row][col]

                if piece:
                    self.board.move(piece, pos, True)
            elif data_type == "quit":
                self.end_text = "Another player disconnected"
                self.board.paused = True

        self.end_text = "Disconnected from the server"
        self.board.paused = True
        self.server.close()

    def disconnect(self):
        print("Disconnect")
        self.server.close()
        del self
