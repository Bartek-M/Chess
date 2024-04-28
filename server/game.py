import random

from public.board import Board


class Game:
    def __init__(self, player: str, code: str) -> None:
        self.players = [player]
        self.board = None
        self.started = False

        self.code = code
        self.color = random.choice(["w", "b"])

    def start(self, player: object) -> None:
        self.players.append(player)
        self.board = Board()
        self.started = True

    def move(self, piece_pos: list[int], pos: list[int]) -> str | None:
        if not (piece_pos and pos):
            return

        row, col = piece_pos
        piece = self.board.board[row][col]

        if not piece:
            return

        piece.valid_moves = [None]
        moved = self.board.move(piece, pos)
        if not moved:
            return

        return {"type": "move", "piece": piece_pos, "pos": pos}

    def get_names(self) -> list[str]:
        players = self.players[::-1] if self.color == "w" else self.players
        return [player.name for player in players]
