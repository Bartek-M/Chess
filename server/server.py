import sys
import json
from threading import Thread
from datetime import datetime, UTC
from socket import socket, AF_INET, SOCK_STREAM

from server.player import Player


class Server:
    players = []
    games = {}

    def __init__(self, host, port, buff_size):
        self.addr = (host, port)
        self.buff_size = buff_size

        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(self.addr)
        self.server.listen()

        print("[SERVER] Started, waiting for connections...")
        self.listen_connections()

    def listen_connections(self):
        conn_thread = Thread(target=self.handle_connect)
        conn_thread.start()

        while True:
            try:
                input()
            except:
                self.close()
                break

    def handle_communication(self, client, player):
        while True:
            try:
                data = client.recv(self.buff_size).decode()
                data = json.loads(data)
                print(data)

                match data.get("type", None):
                    case "hello":
                        name = data.get("name", "Player")
                        code = data.get("code")
                        player.set_data(name, code)
            except:
                self.handle_disconnect(client, player)
                break

    def handle_connect(self):
        while True:
            try:
                client, addr = self.server.accept()
                player = Player(client, addr)
                self.players.append(player)

                print(f"[CONNECTION] {addr} connected at {datetime.now(UTC)}")
                Thread(target=self.handle_communication, args=(client, player)).start()
            except Exception as e:
                print("[ERROR]", e)
                break

        print("[SERVER] Crashed, server has crashed")

    def handle_disconnect(self, client, player):
        client.close()
        self.players.remove(player)
        print(f"[CONNECTION] {player} disconnected at {datetime.now(UTC)}")

    def close(self, *_):
        print("[SERVER] Exit, server has stopped")
        for player in self.players:
            player.client.close()

        self.server.close()
        sys.exit(0)
