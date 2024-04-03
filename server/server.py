import sys
import json
import secrets
import random
from threading import Thread
from datetime import datetime, UTC
from socket import socket, AF_INET, SOCK_STREAM

from server.player import Player
from public.board import Board


class Server:
    players = []
    games = {}
    waiting = set()

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

    def send(self, client, data):
        data = bytes(json.dumps(data), "utf-8")
        client.send(data)

    def receive(self, client, player):
        while True:
            try:
                data = client.recv(self.buff_size).decode("utf-8")
                data = json.loads(data)

                match data.get("type", None):
                    case "hello":
                        name = data.get("name", "Player")
                        code = self.join_lobby(data.get("code"), player, name)
                        player.set_data(name, code)
                    case "move":
                        print(data)
            except Exception as e:
                print("[ERROR]", e)
                self.handle_disconnect(client, player)
                break

    def join_lobby(self, code, player, name, wait=False):
        client = player.client
        game = self.games.get(code)

        if not game or len(game) >= 2:
            if code != "new":
                code = self.waiting.pop() if len(self.waiting) else "new"
                return self.join_lobby(code, player, name, True)

            code = secrets.token_hex(3)
            if wait:
                self.waiting.add(code)

            self.games[code] = [player]
            self.send(client, {"type": "hello", "name": name, "code": code})
            return code

        self.games[code].append(player)
        self.games[code].append(Board())

        if code in self.waiting:
            self.waiting.remove(code)

        color = random.choice(["w", "b"])
        players = (game[0].name, name)
        data = {"type": "connect", "players": players, "color": color}

        self.send(game[0].client, data)
        self.send(game[1].client, {**data, "color": ("b" if color == "w" else "w")})
        return code

    def handle_connect(self):
        while True:
            try:
                client, addr = self.server.accept()
                player = Player(client, addr)
                self.players.append(player)

                print(f"[CONNECTION] {addr} connected at {datetime.now(UTC)}")
                Thread(target=self.receive, args=(client, player)).start()
            except Exception as e:
                break

    def handle_disconnect(self, client, player):
        code = player.code
        if self.games.get(code):
            del self.games[code]
        if code in self.waiting:
            self.waiting.remove(code)

        self.players.remove(player)
        print(f"[CONNECTION] {player} disconnected at {datetime.now(UTC)}")
        client.close()
        del player

    def close(self, *_):
        print("[SERVER] Exit, server has stopped")
        for player in self.players:
            player.client.close()

        self.server.close()
        sys.exit(0)
