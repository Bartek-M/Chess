import time

from public.pieces import King, Queen, Bishop, Knight, Rook, Pawn
from public.utils import translate_pos


class Board:
    def __init__(self, client=None):
        self.color = "w"
        self.board = self.generate_board()
        self.client = client

        self.turn = "w"
        self.players = ("Player 2", "Player 1")
        self.paused = bool(client)

        self.start_time = time.time()
        self.timers = (600, 600)

        self.current = None
        self.passed_pawn = None

    def generate_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        for row in [0, 7]:
            if self.color == "w":
                color = "b" if row == 0 else "w"
                king_col, queen_col = 4, 3
            else:
                color = "b" if row == 7 else "w"
                king_col, queen_col = 3, 4

            pawn_row = row + (-1 if row == 7 else 1)

            board[row][0] = Rook(row, 0, color, 4)
            board[row][1] = Knight(row, 1, color, 3)
            board[row][2] = Bishop(row, 2, color, 2)
            board[row][queen_col] = Queen(row, queen_col, color, 1)
            board[row][king_col] = King(row, king_col, color, 0)
            board[row][5] = Bishop(row, 5, color, 2)
            board[row][6] = Knight(row, 6, color, 3)
            board[row][7] = Rook(row, 7, color, 4)

            for col in range(8):
                board[pawn_row][col] = Pawn(self.color, pawn_row, col, color, 5)

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

        piece.valid_moves = (
            piece.get_moves(self.board, self.passed_pawn)
            if piece.pawn
            else piece.get_moves(self.board)
        )

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
                piece.valid_moves = (
                    piece.get_moves(self.board, self.passed_pawn)
                    if piece.pawn
                    else piece.get_moves(self.board)
                )

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
        self.reset_selected()

        if piece.pawn and y in [0, 7]:
            self.board[y][x] = Queen(y, x, piece.color, 1)
            del piece
            return True

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

        if piece.pawn and abs(piece.row - y) == 2:
            self.passed_pawn = piece
        else:
            self.passed_pawn = None

        self.board[y][x] = piece
        piece.set_pos((x, y))
        self.start_time = time.time()
        return True

    def pause(self):
        if self.client:
            return

        self.paused = not self.paused
        self.start_time = time.time()

    def reset(self, players=("Player 2", "Player 1"), color=None):
        self.players = players if color == "w" else players[::-1]
        self.color = color
        self.board = self.generate_board()

        self.turn = "w"
        self.paused = False

        self.timers = (600, 600)
        self.start_time = time.time()

        self.current = None

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
