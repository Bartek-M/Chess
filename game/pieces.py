class Piece:
    """
    Chess piece representation
    """

    def __init__(self, row: int, col: int, color: str):
        self.row = row
        self.col = col

        self.color = color
        self.selected = False

    def select(self):
        pass


class King(Piece):
    def __repr__(self):
        return "king " + self.color


class Queen(Piece):
    def __repr__(self):
        return "queen " + self.color


class Bishop(Piece):
    def __repr__(self):
        return "bishop " + self.color


class Knight(Piece):
    def __repr__(self):
        return "knight " + self.color


class Rook(Piece):
    def __repr__(self):
        return "rook " + self.color


class Pawn(Piece):
    def __repr__(self):
        return "pawn " + self.color
