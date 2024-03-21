import pygame

from utils import is_avail


class Piece:
    """
    Chess piece representation
    """

    SELECT_COLOR = 56, 220, 255

    def __init__(self, row, col, color, img):
        self.row = row
        self.col = col

        self.color = color  # w | b
        self.img = img
        self.selected = False

        self.king = False
        self.pawn = False

    def draw(self, win, assets, tile_size, padding):
        x = self.col * tile_size + padding[0]
        y = self.row * tile_size + padding[1]

        if self.selected:
            pygame.draw.rect(win, self.SELECT_COLOR, (x, y, tile_size, tile_size), 5)

        win.blit(assets[self.img], (x, y))

    def set_pos(self, pos):
        self.col, self.row = pos


class King(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.king = True

    def valid_moves(self, board):
        moves = []

        return moves

    def __repr__(self):
        return f"king {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Queen(Piece):
    def valid_moves(self, board):
        moves = []

        return moves

    def __repr__(self):
        return f"queen {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Bishop(Piece):
    def valid_moves(self, board):
        moves = []

        return moves

    def __repr__(self):
        return f"bishop {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Knight(Piece):
    def valid_moves(self, board):
        moves = []

        return moves

    def __repr__(self):
        return f"knight {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Rook(Piece):
    def valid_moves(self, board):
        moves = []

        return moves

    def __repr__(self):
        return f"rook {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Pawn(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pawn = True

    def valid_moves(self, board):
        moves = []

        if is_avail(board, (self.col, self.row - 1), self.color) == False:
            moves.append((self.col, self.row - 1))

        if self.row == 6 and is_avail(board, (self.col, self.row - 2), self.color) == False:
            moves.append((self.col, self.row - 2))

        if is_avail(board, (self.col - 1, self.row - 1), self.color):
            moves.append((self.col - 1, self.row - 1))

        if is_avail(board, (self.col + 1, self.row - 1), self.color):
            moves.append((self.col + 1, self.row - 1))

        return moves

    def __repr__(self):
        return f"pawn {self.color} at [{self.row}; {self.col}]; {self.selected}"
