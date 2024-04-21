import os
import time

from public.pieces import King, Queen, Bishop, Knight, Rook, Pawn
from public.utils import translate_pos

TIME = int(os.getenv("TIME", 600))


class Board:
    def __init__(self, client=None):
        self.color = "w"
        self.client = client

        self.turn = "w"
        self.players = ("Player 2", "Player 1")
        self.end_text = None

        self.paused = bool(client)
        self.start_time = time.time()
        self.timers = (TIME, TIME)

        self.current = None
        self.last_moves = []
        self.passed_pawn = None

        self.kings = {"w": None, "b": None}
        self.pieces = {"w": [], "b": []}

        self.board = self.generate_board()

    def generate_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        for row in [0, 7]:
            if self.color == "w":
                color = "b" if row == 0 else "w"
                k_col, q_col = 4, 3
            else:
                color = "b" if row == 7 else "w"
                k_col, q_col = 3, 4

            pawn_row = row + (-1 if row == 7 else 1)

            self.pieces[color] = [
                Rook(self, row, 0, color, 4),
                Knight(self, row, 1, color, 3),
                Bishop(self, row, 2, color, 2),
                Queen(self, row, q_col, color, 1),
                King(self, row, k_col, color, 0),
                Bishop(self, row, 5, color, 2),
                Knight(self, row, 6, color, 3),
                Rook(self, row, 7, color, 4),
            ] + [Pawn(self, pawn_row, col, color, 5) for col in range(8)]

            for piece in self.pieces[color]:
                if type(piece) == King:
                    self.kings[color] = piece

                board[piece.row][piece.col] = piece

        return board

    def select(self, piece):
        if self.current:
            self.current.selected = False
        if self.current == piece:
            return self.reset_selected()

        piece.selected = True
        self.current = piece

        if self.client and piece.color != self.color:
            return
        if piece.color != self.turn or self.paused:
            return

        piece.get_moves()

    def reset_selected(self):
        if not self.current:
            return

        self.current.selected = False
        self.current.first_select = False
        self.current.dragged = False

        self.current.valid_moves = [None]
        self.current = None

    def move(self, piece, pos, checked=False):
        if self.paused:
            return self.reset_selected()

        if not checked:
            if None in piece.valid_moves:
                piece.get_moves()

            if pos not in piece.valid_moves:
                return False

            if self.client:
                piece_pos = (piece.row, piece.col)
                if self.color == "b":
                    piece_pos = translate_pos(piece_pos)
                    pos = translate_pos(pos)

                data = {"type": "move", "piece": piece_pos, "pos": pos}
                return self.client.send(data)

        x, y = pos
        self.board[piece.row][piece.col] = None
        self.turn = "b" if self.turn == "w" else "w"
        self.last_moves = [[piece.col, piece.row], [x, y]]
        self.reset_selected()

        if piece.pawn and y in [0, 7]:
            self.pieces[piece.color].append(Queen(self, y, x, piece.color, 1))
            self.pieces[piece.color].remove(piece)
            piece = self.pieces[piece.color][-1]

        if piece.king or piece.rook:
            piece.moved = True

        if (
            piece.king
            and (new := self.board[y][x])
            and new.rook
            and piece.color == new.color
        ):
            self.board[y][x] = None

            if x > piece.col:
                new_x = x - (3 if piece.col == 3 else 2)
                x = piece.col + 2
            else:
                new_x = x + (2 if piece.col == 3 else 3)
                x = piece.col - 2

            self.board[y][new_x] = new
            new.set_pos((new_x, y))

        if piece.pawn and self.passed_pawn:
            p_pawn = self.passed_pawn
            d = 1 if piece.color == self.color else -1

            if x == p_pawn.col and (y + d) == p_pawn.row:
                self.board[p_pawn.row][p_pawn.col] = None
                del p_pawn

        if piece.pawn and abs(piece.row - y) == 2:
            self.passed_pawn = piece
        else:
            self.passed_pawn = None

        if self.board[y][x]:
            old_piece = self.board[y][x]
            self.pieces[old_piece.color].remove(old_piece)

        self.board[y][x] = piece
        piece.set_pos((x, y))
        self.start_time = time.time()

        self.check_kings()
        return True

    def is_avail(self, pos, piece, board=None):
        x, y = pos
        if not (0 <= x < 8 and 0 <= y < 8):
            return None

        king_check = bool(board)
        board = board if board else self.board
        space = board[y][x]

        if space and space.color == piece.color:
            return None

        if not king_check:
            t_board = [row[:] for row in board]
            t_board[piece.row][piece.col] = None
            t_board[y][x] = piece

            t_pos = (y, x) if piece.king else None
            checked = self.kings[piece.color].is_attacked(t_board, t_pos)

            if checked:
                return "king"

        if space is None:
            return False

        return space

    def check_kings(self):
        checked = self.kings[self.turn].is_attacked()

        for piece in self.pieces[self.turn]:
            piece.get_moves()
            moves = piece.valid_moves

            if None not in moves:
                break
        else:
            if checked:
                self.end_text = f"Checkmate - {'white' if self.turn == 'b' else 'black'} won"
            else:
                self.end_text = "Stealmate - draw"

            self.pause()

    def pause(self):
        if self.client:
            return

        self.paused = not self.paused
        self.start_time = time.time()

    def reset(self, players=("Player 2", "Player 1"), color="w"):
        self.color = color

        self.turn = "w"
        self.players = players if color == "w" else players[::-1]
        self.end_text = None

        self.paused = False
        self.start_time = time.time()
        self.timers = (TIME, TIME)

        self.current = None
        self.last_moves = []
        self.passed_pawn = None

        self.board = self.generate_board()

    def timer(self):
        if self.paused:
            return

        time_1, time_2 = self.timers

        if self.turn == "w":
            time_1 -= time.time() - self.start_time
        else:
            time_2 -= time.time() - self.start_time

        self.start_time = time.time()
        self.timers = time_1, time_2
