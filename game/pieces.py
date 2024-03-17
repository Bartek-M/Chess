import pygame

white_assets = list(
    map(
        lambda img: pygame.transform.scale(img, (128, 128)),
        [
            pygame.image.load("./assets/wk.png"),
            pygame.image.load("./assets/wq.png"),
            pygame.image.load("./assets/wb.png"),
            pygame.image.load("./assets/wn.png"),
            pygame.image.load("./assets/wr.png"),
            pygame.image.load("./assets/wp.png"),
        ],
    )
)

black_assets = list(
    map(
        lambda img: pygame.transform.scale(img, (128, 128)),
        [
            pygame.image.load("./assets/bk.png"),
            pygame.image.load("./assets/bq.png"),
            pygame.image.load("./assets/bb.png"),
            pygame.image.load("./assets/bn.png"),
            pygame.image.load("./assets/br.png"),
            pygame.image.load("./assets/bp.png"),
        ],
    )
)


class Piece:
    """
    Chess piece representation
    """

    def __init__(self, row, col, color):
        self.row = row
        self.col = col

        self.color = color  # w | b
        self.selected = False

    def draw(self, win):
        pass

    def set_pos(self, pos):
        self.row, self.col = pos


class King(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = white_assets[0] if self.color == "w" else black_assets[0]

    def __repr__(self):
        return f"king {self.color} at [{self.row}; {self.col}]"


class Queen(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = white_assets[0] if self.color == "w" else black_assets[0]

    def __repr__(self):
        return f"queen {self.color} at [{self.row}; {self.col}]"


class Bishop(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = white_assets[0] if self.color == "w" else black_assets[0]

    def __repr__(self):
        return f"bishop {self.color} at [{self.row}; {self.col}]"


class Knight(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = white_assets[0] if self.color == "w" else black_assets[0]

    def __repr__(self):
        return f"knight {self.color} at [{self.row}; {self.col}]"


class Rook(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = white_assets[0] if self.color == "w" else black_assets[0]

    def __repr__(self):
        return f"rook {self.color} at [{self.row}; {self.col}]"


class Pawn(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = white_assets[0] if self.color == "w" else black_assets[0]

    def __repr__(self):
        return f"pawn {self.color} at [{self.row}; {self.col}]"
