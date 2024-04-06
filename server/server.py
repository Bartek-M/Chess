import sys
import json
import secrets
from threading import Thread
from datetime import datetime, UTC
from socket import socket, AF_INET, SOCK_STREAM

from server.player import Player
from server.game import Game


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
                        self.join_lobby(data.get("code"), player, name)
                    case "move":
                        game = self.games.get(player.code)
                        if not game or not game.started:
                            continue

                        result = game.move(data.get("piece"), data.get("pos"))
                        if not result:
                            continue

                        for player in game.players:
                            self.send(player.client, result)
            except:
                break

        self.handle_disconnect(client, player)

    def join_lobby(self, code, player, name, wait=False):
        client = player.client
        game = self.games.get(code)

        if not game or game.started:
            if code != "new":
                code = self.waiting.pop() if len(self.waiting) else "new"
                return self.join_lobby(code, player, name, True)

            code = secrets.token_hex(3)
            if wait:
                self.waiting.add(code)

            player.set_data(name, code)
            self.games[code] = Game(player, code)
            return self.send(client, {"type": "hello", "name": name, "code": code})

        if code in self.waiting:
            self.waiting.remove(code)

        player.set_data(name, code)
        game.start(player)
        data = {"type": "connect", "players": game.get_names(), "color": game.color}
        color_2 = "b" if game.color == "w" else "w"

        self.send(game.players[0].client, data)
        self.send(game.players[1].client, {**data, "color": color_2})

    def handle_connect(self):
        while True:
            try:
                client, addr = self.server.accept()
                player = Player(client, addr)
                self.players.append(player)
                Thread(target=self.receive, args=(client, player)).start()
            except Exception as e:
                break

    def handle_disconnect(self, client, player):
        code = player.code
        game = self.games.get(code)

        if game:
            for p in game.players:
                if p == player:
                    continue
                self.send(p.client, {"type": "quit"})

            del self.games[code]

        if code in self.waiting:
            self.waiting.remove(code)

        if player in self.players:
            self.players.remove(player)
            del player

        client.close()

    def close(self):
        print("[SERVER] Exit, server has stopped")
        for player in self.players:
            player.client.close()

        self.server.close()
        sys.exit(0)
