import pygame


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

    def draw(self, win, tile_size):
        win.blit(self.img, (tile_size * self.col, tile_size * self.row))

        if not self.selected:
            return

        x, y = self.col * tile_size, self.row * tile_size
        pygame.draw.rect(win, self.SELECT_COLOR, (x, y, tile_size, tile_size), 5)

    def set_pos(self, pos):
        self.row, self.col = pos


class King(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.king = True

    def valid_moves(self, board) -> tuple:
        moves = ()

        return moves

    def __repr__(self):
        return f"king {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Queen(Piece):
    def valid_moves(self, board) -> tuple:
        moves = ()

        return moves

    def __repr__(self):
        return f"queen {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Bishop(Piece):
    def valid_moves(self, board) -> tuple:
        moves = ()

        return moves

    def __repr__(self):
        return f"bishop {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Knight(Piece):
    def valid_moves(self, board) -> tuple:
        moves = ()

        return moves

    def __repr__(self):
        return f"knight {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Rook(Piece):
    def valid_moves(self, board) -> tuple:
        moves = ()

        return moves

    def __repr__(self):
        return f"rook {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Pawn(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pawn = True

    def valid_moves(self, board) -> tuple:
        moves = ()

        return moves

    def __repr__(self):
        return f"pawn {self.color} at [{self.row}; {self.col}]; {self.selected}"
