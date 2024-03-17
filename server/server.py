import os
from threading import Thread
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM

import dotenv

from player import Player

dotenv.load_dotenv()

HOST = os.getenv("HOST", "127.0.0.1")
PORT = os.getenv("PORT", 5000)
BUFF_SIZE = os.getenv("BUFF_SIZE", 512)


class Server:
    players = []

    def __init__(self):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen()

        print("[SERVER] Started, waiting for connections...")
        self.listen_connections()

    def listen_connections(self):
        conn_thread = Thread(target=self.handle_connect)
        conn_thread.start()
        conn_thread.join()

        self.server.close()
        print("[SERVER] Exit, server has stopped")

    def handle_connect(self):
        while True:
            try:
                client, addr = self.server.accept()
                player = Player(addr, client)
                self.players.append(player)

                print(f"[CONNECTION] {addr} connected at {datetime.now(datetime.UTC)}")
                Thread(target=None, args=(player,)).start()
            except Exception as e:
                print("[ERROR]", e)
                break

        print("[SERVER] Crashed, server has crashed")

    def handle_disconnect(self):
        pass
