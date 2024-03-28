import random

from public.pieces import Queen
from public.utils import generate_board


class Board:
    def __init__(self, fps):
        self.fps = fps

        self.color = random.choice(("w", "b"))
        self.board = generate_board(self.color)
        self.timers = (600, 600)

        self.current = None
        self.valid_moves = []

    def select(self, piece):
        if self.current:
            self.current.selected = False

        if self.current == piece:
            return self.reset_selected()

        piece.selected = True
        self.current = piece
        self.valid_moves = piece.valid_moves(self.board)

    def reset_selected(self):
        if not self.current:
            return

        self.current.selected = False
        self.current.first_select = False
        self.current.dragged = False

        self.current = None
        self.valid_moves = []

    def move(self, piece, pos):
        x, y = pos

        self.board[piece.row][piece.col] = None
        self.reset_selected()

        if piece.pawn and y in [0, 7]:
            self.board[y][x] = Queen(y, x, piece.color, 1)
            del piece
            return

        if piece.king or piece.rook:
            piece.moved = True

        if piece.king and (new := self.board[y][x]) and new.rook:
            self.board[y][x] = None

            if x > piece.col:
                new_x = x - (3 if piece.col == 3 else 2)
                x = piece.col + 2
            else:
                new_x = x + (2 if piece.col == 3 else 3)
                x = piece.col - 2

            self.board[y][new_x] = new
            new.set_pos((new_x, y))

        self.board[y][x] = piece
        piece.set_pos((x, y))

    def reset(self):
        pass

    def timer(self):
        time_1, time_2 = self.timers
        self.timers = (time_1 - 1 / self.fps, time_2 - 1 / self.fps)
