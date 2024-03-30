from public.pieces import Queen
from public.utils import generate_board


class Board:
    def __init__(self, color="w"):
        self.color = color
        self.board = generate_board(self.color)

        self.turn = "w"
        self.timers = (600, 600)
        self.paused = False
        self.current = None

    def select(self, piece):
        if self.current:
            self.current.selected = False

        if self.current == piece:
            return self.reset_selected()

        piece.selected = True
        self.current = piece

        if self.turn == piece.color:
            piece.valid_moves = piece.get_moves(self.board)

    def reset_selected(self):
        if not self.current:
            return

        self.current.selected = False
        self.current.first_select = False
        self.current.dragged = False

        self.current.valid_moves = [None]
        self.current = None

    def move(self, piece, pos):
        if self.paused:
            return self.reset_selected()

        if None in piece.valid_moves:
            piece.valid_moves = piece.get_moves(self.board)

        if pos not in piece.valid_moves:
            return

        x, y = pos
        self.board[piece.row][piece.col] = None
        self.turn = "b" if self.turn == "w" else "w"
        self.reset_selected()

        if piece.pawn and y in [0, 7]:
            self.board[y][x] = Queen(y, x, piece.color, 1)
            del piece
            return

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

        self.board[y][x] = piece
        piece.set_pos((x, y))

    def pause(self):
        self.paused = not self.paused

    def reset(self):
        self.board = generate_board(self.color)
        self.timers = (600, 600)
        self.turn = "w"
        self.current = None

    def timer(self, fps):
        if self.paused:
            return

        time_1, time_2 = self.timers
        self.timers = (
            (time_1 - 1 / fps, time_2)
            if self.turn == "w"
            else (time_1, time_2 - 1 / fps)
        )
